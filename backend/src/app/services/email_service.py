from sqlalchemy.orm import Session
from ..models.email import Email
from ..services.google_service import get_gmail_service
from ..services.groq_service import summarize_text
import base64
from bs4 import BeautifulSoup

def fetch_and_store_emails(db: Session, user_id: int):
    """
    Connects to the Gmail API, fetches unread emails, summarizes them,
    and stores them in the database.
    """
    print("Executing email search job...")
    
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', q="is:unread", maxResults=10).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No new unread messages found.")
            return

        print(f"Found {len(messages)} unread messages. Processing...")
        for message_info in messages:
            msg = service.users().messages().get(userId='me', id=message_info['id'], format='full').execute()
            
            message_id = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Message-ID'), None)
            
            # Skip if email already exists in DB
            if db.query(Email).filter(Email.message_id == message_id).first():
                continue

            subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
            sender = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), 'Unknown Sender')
            recipient = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'To'), 'Unknown Recipient')
            
            body_data = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body_data = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            else:
                 if 'data' in msg['payload']['body']:
                    body_data = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

            # Summarize the body
            summary = summarize_text(f"Summarize the following email body in one or two sentences:\n\n---\n{body_data[:2000]}\n---")

            new_email = Email(
                message_id=message_id,
                subject=subject,
                sender=sender,
                recipient=recipient,
                body=body_data,
                summary=summary,
                is_read=False,
                owner_id=user_id 
            )
            db.add(new_email)

        db.commit()
        print(f"Successfully stored {len(messages)} new emails.")

    except Exception as e:
        print(f"Could not fetch emails. Error: {e}")

    print("Email search job finished.")