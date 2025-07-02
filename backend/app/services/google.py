import os
import httpx
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from typing import Optional, Dict, Tuple
from sqlalchemy.orm import Session
from .. import models

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'openid'
]

def get_flow():
    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
            }
        },
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )

# Função corrigida para retornar as informações e as credenciais
def exchange_code_for_user_info(code: str) -> Optional[Tuple[Dict, Credentials]]:
    flow = get_flow()
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials

        async def get_info():
            async with httpx.AsyncClient() as client:
                headers = {'Authorization': f'Bearer {credentials.token}'}
                response = await client.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
                response.raise_for_status()
                return response.json()

        user_info = httpx.run(get_info)
        return user_info, credentials
    except Exception as e:
        print(f"Failed to exchange code or get user info from Google: {e}")
        return None

def create_google_auth_url() -> str:
    flow = get_flow()
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return authorization_url

def get_google_user_info(code: str, db: Session) -> Optional[Dict]:
    flow = get_flow()
    try:
        flow.fetch_token(code=code)
        credentials = flow.credentials

        async def get_info():
            async with httpx.AsyncClient() as client:
                headers = {'Authorization': f'Bearer {credentials.token}'}
                response = await client.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
                response.raise_for_status()
                return response.json()

        user_info = httpx.run(get_info)

        user = db.query(models.User).filter(models.User.email == user_info['email']).first()
        if user:
            user.access_token = credentials.token
            user.refresh_token = credentials.refresh_token
            db.commit()

        return user_info
    except Exception as e:
        print(f"Failed to get user info from Google: {e}")
        return None

def get_credentials_for_user(user: models.User) -> Optional[Credentials]:
    if not user.access_token:
        return None
    return Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )

async def sync_google_calendar(db: Session, user: models.User):
    creds = get_credentials_for_user(user)
    if not creds:
        return {"error": "User not authenticated with Google"}

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Aqui você implementaria a lógica para salvar/atualizar os eventos no seu DB
        # Ex: for event in events: crud.create_or_update_event(db, event, user.id)
        
        return {"status": "success", "events_found": len(events)}
    except Exception as e:
        print(f"An error occurred syncing calendar: {e}")
        return {"error": str(e)}

async def sync_google_emails(db: Session, user: models.User):
    creds = get_credentials_for_user(user)
    if not creds:
        return {"error": "User not authenticated with Google"}
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread", maxResults=10).execute()
        messages = results.get('messages', [])
        
        # Aqui você implementaria a lógica para salvar/analisar os emails
        # Ex: for msg in messages: process_email(db, msg, user.id)
        
        return {"status": "success", "messages_found": len(messages)}
    except Exception as e:
        print(f"An error occurred syncing emails: {e}")
        return {"error": str(e)}