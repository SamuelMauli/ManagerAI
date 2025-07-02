import base64
import datetime
import os
import re
from typing import Dict, Optional, Tuple, List, Any

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError as HttpAccessTokenRefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..config import settings

SCOPES = settings.GOOGLE_SCOPES.split(',')


def _get_email_body(payload: Dict[str, Any]) -> str:
    """Extrai o corpo de texto de um payload de e-mail do Gmail recursivamente."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
            
            # Fallback recursivo para partes aninhadas (multipart/alternative)
            if "parts" in part:
                body = _get_email_body(part)
                if body:
                    return body
                    
    if "body" in payload and "data" in payload["body"]:
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        
    return ""


def exchange_code_for_credentials(code: str) -> Optional[Tuple[Dict[str, Any], Credentials]]:
    try:
        client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        
        flow = Flow.from_client_config(
            client_config=client_config,
            scopes=SCOPES,
            redirect_uri='postmessage'
        )

        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        return user_info, credentials

    except Exception as e:
        print(f"!!! FALHA NA TROCA DO CÓDIGO: {e}")
        return None


def refresh_access_token_if_needed(db: Session, user: models.User) -> bool:
    if not user.refresh_token:
        return False

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES
    )

    if not credentials.expired or not credentials.refresh_token:
        return True
        
    try:
        print(f"Atualizando token de acesso para {user.email}...")
        credentials.refresh(Request())
        user.access_token = credentials.token
        user.expires_at = credentials.expiry
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Token de acesso atualizado com sucesso para {user.email}.")
        return True
    except HttpAccessTokenRefreshError as e:
        print(f"Erro ao atualizar token para {user.email}: {e}")
        user.access_token = None
        user.refresh_token = None
        user.expires_at = None
        db.add(user)
        db.commit()
        return False


def sync_google_emails(db: Session, user_id: int):
    user = crud.get_user(db, user_id=user_id)
    if not (user and user.access_token):
        print(f"Usuário {user_id} não encontrado ou sem token de acesso.")
        return

    if not refresh_access_token_if_needed(db, user):
        print(f"Não foi possível sincronizar e-mails para {user_id} devido a problema com o token.")
        return

    try:
        credentials = Credentials.from_authorized_user_info({
            "token": user.access_token,
            "refresh_token": user.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": SCOPES
        })
        
        service: Resource = build('gmail', 'v1', credentials=credentials)
        print(f"Iniciando sincronização de e-mails para: {user.email}")
        
        results = service.users().messages().list(userId='me', maxResults=50).execute()
        messages = results.get('messages', [])

        if not messages:
            print("Nenhum e-mail novo encontrado para sincronizar.")
            return
            
        new_emails_to_add = []
        for msg in messages:
            msg_id = msg['id']
            if crud.get_email_by_google_id(db, google_email_id=msg_id, user_id=user.id):
                continue

            msg_full = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            
            headers = msg_full['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'Sem Assunto')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Desconhecido')
            
            body_content = _get_email_body(msg_full['payload'])
            
            received_at_ts = int(msg_full['internalDate']) / 1000
            received_at = datetime.datetime.fromtimestamp(received_at_ts)

            email_schema = schemas.EmailCreate(
                email_id=msg_id,
                thread_id=msg['threadId'],
                subject=subject,
                sender=sender,
                snippet=msg_full.get('snippet', ''),
                body=body_content,
                is_read='UNREAD' not in msg_full.get('labelIds', []),
                received_at=received_at
            )
            
            new_emails_to_add.append(email_schema)

        if not new_emails_to_add:
            print(f"Todos os {len(messages)} e-mails recentes já estavam sincronizados.")
            return
            
        crud.create_multiple_user_emails(db, emails=new_emails_to_add, user_id=user.id)
        print(f"{len(new_emails_to_add)} novos e-mails salvos no banco de dados para {user.email}.")

    except HttpError as error:
        print(f"Ocorreu um erro na API do Gmail: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao sincronizar e-mails: {e}")