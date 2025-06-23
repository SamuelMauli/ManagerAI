from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..services.google_service import get_gmail_service
from ..services.youtrack_service import get_youtrack_service
from ..services.groq_service import summarize_text

router = APIRouter()

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Fetches statistics for the dashboard: unread emails, pending tasks, and active projects.
    """
    # Gmail
    gmail_service = get_gmail_service()
    email_results = gmail_service.users().messages().list(userId='me', q="is:unread").execute()
    unread_emails_count = email_results.get('resultSizeEstimate', 0)

    # YouTrack
    youtrack_service = get_youtrack_service()
    # Note: You will need to implement these functions in your youtrack_service.py
    pending_tasks_count = youtrack_service.get_pending_tasks_count() 
    active_projects_count = youtrack_service.get_active_projects_count()

    return {
        "unread_emails": unread_emails_count,
        "pending_tasks": pending_tasks_count,
        "active_projects": active_projects_count
    }

@router.get("/dashboard/summarized-emails")
async def get_summarized_emails():
    """
    Fetches unread emails, summarizes them using Groq, and returns them.
    """
    gmail_service = get_gmail_service()
    messages = gmail_service.users().messages().list(userId='me', q="is:unread", maxResults=5).execute().get('messages', [])
    
    summarized_emails = []
    for message in messages:
        msg = gmail_service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        
        subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
        sender = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), 'Unknown Sender')
        snippet = msg['snippet']

        # Create a prompt for summarization
        prompt = f"Summarize the following email snippet in one sentence:\n\nSnippet: {snippet}"
        summary = await summarize_text(prompt) # We'll create this service next

        summarized_emails.append({
            "id": msg['id'],
            "subject": subject,
            "sender": sender,
            "summary": summary
        })

    return summarized_emails