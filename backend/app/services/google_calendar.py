# backend/app/services/google_calendar.py

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
from typing import List, Dict, Any
from .. import models, crud
from sqlalchemy.orm import Session

def get_credentials_from_user(user: models.User, db: Session) -> Credentials | None:
    """Busca o token do Google do usuário no banco de dados e cria as credenciais."""
    google_token = crud.get_google_token(db, user_id=user.id)
    if not google_token:
        return None
    
    # Recria o objeto de credenciais. Faltam alguns dados, mas é um bom começo.
    # O ideal é ter client_id, client_secret e token_uri para o refresh.
    return Credentials(
        token=google_token.access_token,
        refresh_token=google_token.refresh_token,
        # Adicione aqui os dados do seu client_secret se precisar de refresh
    )

async def get_user_events_today(user: models.User, db: Session) -> str:
    """Busca os eventos de hoje do usuário."""
    creds = get_credentials_from_user(user, db)
    if not creds:
        return "Não foi possível encontrar suas credenciais do Google. Por favor, faça o login novamente."

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True, orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    if not events:
        return "Você não tem nenhum evento na sua agenda para hoje."

    event_list = "\n".join([f"- {event['summary']} às {datetime.datetime.fromisoformat(event['start'].get('dateTime')).strftime('%H:%M')}" for event in events if 'dateTime' in event['start']])
    return f"Seus compromissos para hoje são:\n{event_list}"

# ... outras funções do calendário ...