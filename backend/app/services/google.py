import base64
import datetime
import os
import re
from typing import Dict, Optional, Tuple, List, Any
from email.message import EmailMessage # Adicionar esta importação

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError as HttpAccessTokenRefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow 
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..config import settings
from .. import models

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
                google_email_id=msg_id,
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

# NOVO: Função para enviar e-mails
def send_email(db: Session, user: models.User, email_data: schemas.EmailSendRequest) -> Dict[str, Any]:
    if not refresh_access_token_if_needed(db, user):
        raise Exception("Não foi possível enviar e-mail: problema com o token.")

    try:
        credentials = Credentials.from_authorized_user_info({
            "token": user.access_token,
            "refresh_token": user.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": SCOPES # Certifique-se de que o escopo de envio ('https://www.googleapis.com/auth/gmail.send') esteja incluído em settings.GOOGLE_SCOPES
        })
        service: Resource = build('gmail', 'v1', credentials=credentials)

        message = EmailMessage()
        message['To'] = email_data.to
        message['From'] = user.email # Remetente será o próprio usuário
        message['Subject'] = email_data.subject
        
        if email_data.is_html:
            message.set_content(email_data.body, subtype='html')
        else:
            message.set_content(email_data.body)

        if email_data.in_reply_to_id:
            message['In-Reply-To'] = email_data.in_reply_to_id
        if email_data.thread_id:
            message['References'] = email_data.thread_id # Usar References para threads existentes

        # Codificar a mensagem para o formato base64url
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message,
            'threadId': email_data.thread_id if email_data.thread_id else None
        }
        
        sent_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"E-mail enviado! ID da Mensagem: {sent_message['id']}")
        return sent_message

    except HttpError as error:
        print(f"Ocorreu um erro na API do Gmail ao enviar: {error}")
        raise Exception(f"Falha ao enviar e-mail: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao enviar e-mail: {e}")
        raise Exception(f"Erro inesperado ao enviar e-mail: {e}")


def get_events_for_today(db: Session, user: models.User) -> List[Dict]:
    """
    Busca os eventos do Google Calendar para o usuário no dia de hoje.
    """
    if not refresh_access_token_if_needed(db, user):
        print(f"Não foi possível buscar eventos para o usuário {user.id} devido a problema com o token.")
        return []

    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES
    )
    
    service = build('calendar', 'v3', credentials=credentials)
    
    # Define o intervalo de tempo para o dia de hoje
    now = datetime.datetime.utcnow()
    time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    time_max = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=time_min,
        timeMax=time_max,
        maxResults=10, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        formatted_events.append({
            "id": event['id'],
            "summary": event['summary'],
            "start_time": start,
            "end_time": end,
        })
        
    return formatted_events

# NOVO: Função para criar evento no calendário
def create_calendar_event(db: Session, user: models.User, event_data: schemas.CalendarEventCreate) -> Dict[str, Any]:
    if not refresh_access_token_if_needed(db, user):
        raise Exception("Não foi possível criar evento: problema com o token.")
    
    try:
        credentials = Credentials.from_authorized_user_info({
            "token": user.access_token,
            "refresh_token": user.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": SCOPES # Certifique-se de que o escopo de calendário ('https://www.googleapis.com/auth/calendar.events') esteja incluído
        })
        service: Resource = build('calendar', 'v3', credentials=credentials)

        event = {
            'summary': event_data.summary,
            'description': event_data.description,
            'start': {
                'dateTime': event_data.start_time.isoformat(),
                'timeZone': event_data.time_zone,
            },
            'end': {
                'dateTime': event_data.end_time.isoformat(),
                'timeZone': event_data.time_zone,
            },
            'attendees': [{'email': att} for att in event_data.attendees] if event_data.attendees else [],
            'reminders': {
                'useDefault': True,
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Evento criado: {created_event.get('htmlLink')}")
        return created_event

    except HttpError as error:
        print(f"Ocorreu um erro na API do Google Calendar ao criar evento: {error}")
        raise Exception(f"Falha ao criar evento no calendário: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao criar evento: {e}")
        raise Exception(f"Erro inesperado ao criar evento: {e}")

# NOVO: Função para atualizar evento no calendário
def update_calendar_event(db: Session, user: models.User, event_id: str, event_data: schemas.CalendarEventUpdate) -> Dict[str, Any]:
    if not refresh_access_token_if_needed(db, user):
        raise Exception("Não foi possível atualizar evento: problema com o token.")
    
    try:
        credentials = Credentials.from_authorized_user_info({
            "token": user.access_token,
            "refresh_token": user.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": SCOPES
        })
        service: Resource = build('calendar', 'v3', credentials=credentials)

        # Primeiro, obtenha o evento existente para não sobrescrever campos não fornecidos
        existing_event = service.events().get(calendarId='primary', eventId=event_id).execute()

        # Atualiza apenas os campos fornecidos
        if event_data.summary is not None:
            existing_event['summary'] = event_data.summary
        if event_data.description is not None:
            existing_event['description'] = event_data.description
        if event_data.start_time is not None:
            existing_event['start']['dateTime'] = event_data.start_time.isoformat()
            if event_data.time_zone is not None:
                existing_event['start']['timeZone'] = event_data.time_zone
        if event_data.end_time is not None:
            existing_event['end']['dateTime'] = event_data.end_time.isoformat()
            if event_data.time_zone is not None:
                existing_event['end']['timeZone'] = event_data.time_zone
        if event_data.attendees is not None:
            existing_event['attendees'] = [{'email': att} for att in event_data.attendees]
            
        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=existing_event).execute()
        print(f"Evento atualizado: {updated_event.get('htmlLink')}")
        return updated_event

    except HttpError as error:
        print(f"Ocorreu um erro na API do Google Calendar ao atualizar evento: {error}")
        raise Exception(f"Falha ao atualizar evento no calendário: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao atualizar evento: {e}")
        raise Exception(f"Erro inesperado ao atualizar evento: {e}")

def search_drive_files(user: models.User, query: str, max_results: int = 10):
    """Busca arquivos no Google Drive do usuário."""
    if not user.access_token:
        return "Usuário não autenticado."

    creds = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    try:
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(
            q=f"name contains '{query}' and 'me' in owners and trashed=false",
            pageSize=max_results,
            fields="nextPageToken, files(id, name, webViewLink, createdTime, mimeType)" # Adicionado mimeType
        ).execute()
        
        items = results.get('files', [])
        if not items:
            return "Nenhum arquivo encontrado com esse termo."
            
        return [
            {
                "id": item['id'], # Adicionado ID
                "name": item['name'],
                "mime_type": item['mimeType'], # Adicionado mime_type
                "link": item['webViewLink'],
                "created_time": item['createdTime']
            } for item in items
        ]
    except Exception as e:
        print(f"Erro ao buscar arquivos no Google Drive: {e}")
        return f"Ocorreu um erro ao acessar o Google Drive: {e}"

# NOVO: Função para obter o conteúdo de um arquivo do Google Drive
def get_drive_file_content(db: Session, user: models.User, file_id: str) -> Optional[schemas.DriveFileContent]:
    if not refresh_access_token_if_needed(db, user):
        raise Exception("Não foi possível obter o conteúdo do arquivo: problema com o token.")
    
    try:
        credentials = Credentials.from_authorized_user_info({
            "token": user.access_token,
            "refresh_token": user.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": SCOPES # Certifique-se de que o escopo apropriado para Drive ('https://www.googleapis.com/auth/drive.readonly' ou 'https://www.googleapis.com/auth/drive') esteja incluído
        })
        service: Resource = build('drive', 'v3', credentials=credentials)

        file_metadata = service.files().get(fileId=file_id, fields="name, mimeType").execute()
        file_name = file_metadata.get('name')
        mime_type = file_metadata.get('mimeType')

        # Para documentos do Google Workspace (Docs, Sheets, Slides), é necessário exportar
        if mime_type == 'application/vnd.google-apps.document':
            # Exportar como texto simples ou HTML para processamento
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
            request = service.files().export_media(fileId=file_id, mimeType='text/csv') # Ou outro formato adequado
        elif mime_type == 'application/vnd.google-apps.presentation':
            request = service.files().export_media(fileId=file_id, mimeType='text/plain') # Ou outro formato adequado
        elif mime_type.startswith('text/') or mime_type == 'application/pdf': # PDFs não podem ser exportados, mas podem ser baixados se o Drive API permitir (requer tratamento de PDF)
             request = service.files().get_media(fileId=file_id)
        else:
            # Para outros tipos de arquivo, tentar baixar diretamente
            request = service.files().get_media(fileId=file_id)

        content = request.execute().decode('utf-8') # Decodificar para string

        return schemas.DriveFileContent(file_id=file_id, file_name=file_name, mime_type=mime_type, content=content)

    except HttpError as error:
        print(f"Ocorreu um erro na API do Google Drive ao obter conteúdo do arquivo: {error}")
        raise Exception(f"Falha ao obter conteúdo do arquivo do Drive: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao obter conteúdo do arquivo: {e}")
        raise Exception(f"Erro inesperado ao obter conteúdo do arquivo: {e}")

# NOVO: Função para criar arquivo no Google Drive
def create_drive_file(db: Session, user: models.User, file_name: str, mime_type: str, content: str) -> Dict[str, Any]:
    if not refresh_access_token_if_needed(db, user):
        raise Exception("Não foi possível criar arquivo: problema com o token.")
    
    try:
        credentials = Credentials.from_authorized_user_info({
            "token": user.access_token,
            "refresh_token": user.refresh_token,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "scopes": SCOPES # Certifique-se de que o escopo apropriado para Drive ('https://www.googleapis.com/auth/drive') esteja incluído
        })
        service: Resource = build('drive', 'v3', credentials=credentials)

        file_metadata = {
            'name': file_name,
            'mimeType': mime_type
        }
        media_body = {'mimeType': mime_type, 'body': content} # Content as bytes or string

        created_file = service.files().create(
            body=file_metadata,
            media_body=content, # Passar o conteúdo aqui
            fields='id, name, webViewLink, mimeType'
        ).execute()

        print(f"Arquivo criado no Drive: {created_file.get('webViewLink')}")
        return created_file

    except HttpError as error:
        print(f"Ocorreu um erro na API do Google Drive ao criar arquivo: {error}")
        raise Exception(f"Falha ao criar arquivo no Drive: {error}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao criar arquivo: {e}")
        raise Exception(f"Erro inesperado ao criar arquivo: {e}")