import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes for the services you want to access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

def get_google_creds():
    """
    Authenticates with Google and returns credentials.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_gmail_service():
    """
    Returns a Gmail API service object.
    """
    creds = get_google_creds()
    return build('gmail', 'v1', credentials=creds)

def get_calendar_service():
    """
    Returns a Google Calendar API service object.
    """
    creds = get_google_creds()
    return build('calendar', 'v3', credentials=creds)

def get_drive_service():
    """
    Returns a Google Drive API service object.
    """
    creds = get_google_creds()
    return build('drive', 'v3', credentials=creds)