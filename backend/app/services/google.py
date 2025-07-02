import datetime
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from google.auth.exceptions import RefreshError as HttpAccessTokenRefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..config import settings
import base64
import re
from typing import Optional, Tuple, Dict # Adicione Optional, Tuple, Dict aqui


SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
]

def exchange_code_for_credentials(code: str) -> Optional[Tuple[Dict, Credentials]]:
    try:
        client_config = {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
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

def refresh_access_token_if_needed(db: Session, user: models.User):
    if not user.refresh_token:
        print(f"Usuário {user.email} não possui refresh_token. Não é possível atualizar.")
        return False

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=settings.GOOGLE_SCOPES.split(',')
    )

    if credentials.expired and credentials.refresh_token:
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
            # Considerar invalidar o token do usuário ou forçar novo login
            user.access_token = None
            user.refresh_token = None
            user.expires_at = None
            db.add(user)
            db.commit()
            return False
    return True # Token ainda válido ou não precisa de refresh

def sync_google_emails(db: Session, user_id: int):
    user = crud.get_user(db, user_id=user_id)
    if not user or not user.access_token:
        print(f"Usuário {user_id} não encontrado ou sem token de acesso.")
        return

    # Tenta atualizar o token de acesso antes de prosseguir
    if not refresh_access_token_if_needed(db, user):
        print(f"Não foi possível sincronizar e-mails para o usuário {user_id} devido a problema com o token.")
        return

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=settings.GOOGLE_SCOPES.split(',')
    )

    try:
        service = build('gmail', 'v1', credentials=credentials)
        print(f"Iniciando sincronização de e-mails para o usuário: {user.email}")

        # Busca as mensagens mais recentes (ex: 50 mensagens)
        # Você pode ajustar a query para 'is:unread' para apenas e-mails não lidos,
        # ou outras queries para filtrar.
        results = service.users().messages().list(userId='me', maxResults=50).execute()
        messages = results.get('messages', [])

        if not messages:
            print("Nenhum e-mail encontrado.")
            return

        for msg in messages:
            msg_id = msg['id']
            thread_id = msg['threadId']

            # Verifica se o email já existe no banco de dados para evitar duplicatas
            existing_email = crud.get_email_by_google_id(db, google_email_id=msg_id, user_id=user.id)
            if existing_email:
                # print(f"Email {msg_id} já existe no banco de dados. Pulando.")
                continue

            msg_full = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            headers = msg_full['payload']['headers']

            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'Sem Assunto')
            sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Desconhecido')

            snippet = msg_full.get('snippet', '')
            received_at_timestamp = int(msg_full['internalDate']) / 1000  # Convert ms to seconds
            received_at = datetime.datetime.fromtimestamp(received_at_timestamp)

            body_content = ""
            if 'parts' in msg_full['payload']:
                for part in msg_full['payload']['parts']:
                    if part['mimeType'] == 'text/plain' and 'body' in part and 'data' in part['body']:
                        body_content = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                    elif part['mimeType'] == 'text/html' and 'body' in part and 'data' in part['body']:
                        # Para HTML, você pode querer um parser mais robusto
                        # Por enquanto, vamos tentar decodificar e limpar tags HTML
                        html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        body_content = re.sub('<[^>]*>', '', html_body) # Remove tags HTML básicas
                        break
            elif 'body' in msg_full['payload'] and 'data' in msg_full['payload']['body']:
                 body_content = base64.urlsafe_b64decode(msg_full['payload']['body']['data']).decode('utf-8')


            email_data = schemas.EmailCreate(
                email_id=msg_id,
                thread_id=thread_id,
                subject=subject,
                sender=sender,
                snippet=snippet,
                body=body_content,
                is_read=False # Você pode verificar o status de leitura real na API
            )

            # Define o 'received_at' explicitamente para garantir que seja salvo corretamente
            db_email = crud.create_user_email(db, email=email_data, user_id=user.id)
            db_email.received_at = received_at # Sobrescreve o default com a data real do email
            db.add(db_email)
            db.commit()
            print(f"Email '{subject}' de '{sender}' salvo no banco de dados.")

    except HttpError as error:
        print(f"Ocorreu um erro na API do Gmail: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao sincronizar e-mails: {e}")