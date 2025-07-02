# backend/app/services/google.py
import os
from typing import Optional, Tuple, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Escopos definem as permissões que sua aplicação solicita ao usuário.
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
]

def exchange_code_for_credentials(code: str) -> Optional[Tuple[Dict, Credentials]]:
    """
    Função central para autenticação.
    Recebe o código de autorização do frontend, troca-o por credenciais
    e busca as informações básicas do perfil do usuário.
    """
    try:
        # Configuração do fluxo OAuth usando variáveis de ambiente
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=SCOPES,
            # 'postmessage' é o redirect_uri correto para o fluxo 'auth-code' do frontend
            redirect_uri='postmessage'
        )

        # Troca o código recebido por um token de acesso e um refresh token
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Usa as credenciais para obter as informações do usuário
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()

        # Retorna as informações do perfil e as credenciais completas
        return user_info, credentials

    except Exception as e:
        # Log detalhado em caso de falha na comunicação com o Google
        print(f"!!! FALHA NA TROCA DO CÓDIGO: {e}")
        return None

def get_credentials_from_user(user) -> Optional[Credentials]:
    """
    Recria um objeto de credenciais a partir dos tokens salvos no banco de dados.
    Este objeto é capaz de se auto-refrescar se o token de acesso expirar.
    """
    if not user.access_token or not user.refresh_token:
        return None

    return Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES
    )

def sync_google_calendar(user) -> Dict:
    """
    Busca os próximos eventos do Google Calendar para um usuário autenticado.
    """
    credentials = get_credentials_from_user(user)
    if not credentials:
        return {"error": "Credenciais do usuário não encontradas."}

    try:
        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.utcnow().isoformat() + 'Z'  # Formato UTC
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=15,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return {"status": "success", "events": events}

    except HttpError as e:
        print(f"Erro na API do Google Calendar: {e}")
        return {"error": f"Erro na API: {e.reason}"}
    except Exception as e:
        print(f"Erro inesperado ao sincronizar calendário: {e}")
        return {"error": "Erro inesperado ao sincronizar calendário."}

def sync_google_emails(user) -> Dict:
    """
    Busca os e-mails não lidos do Gmail para um usuário autenticado.
    """
    credentials = get_credentials_from_user(user)
    if not credentials:
        return {"error": "Credenciais do usuário não encontradas."}

    try:
        service = build('gmail', 'v1', credentials=credentials)
        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q="is:unread",
            maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        return {"status": "success", "messages": messages}

    except HttpError as e:
        print(f"Erro na API do Gmail: {e}")
        return {"error": f"Erro na API: {e.reason}"}
    except Exception as e:
        print(f"Erro inesperado ao sincronizar e-mails: {e}")
        return {"error": "Erro inesperado ao sincronizar e-mails."}