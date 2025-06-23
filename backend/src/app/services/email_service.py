from sqlalchemy.orm import Session
from ..models.setting import Setting
from ..core.security import encrypt_data, decrypt_data
from ..schemas.setting import EmailConfig
from .google_service import get_gmail_service # Assuming google_service is set up

def save_email_config(db: Session, config: EmailConfig):
    # This function is an example of how you might save encrypted settings
    # You would call this from a settings API endpoint
    encrypted_user = encrypt_data(config.smtp_user)
    encrypted_pass = encrypt_data(config.smtp_pass)
    
    db_user = db.query(Setting).filter(Setting.key == "smtp_user").first()
    if db_user:
        db_user.value = encrypted_user
    else:
        db_user = Setting(key="smtp_user", value=encrypted_user)
        db.add(db_user)

    db_pass = db.query(Setting).filter(Setting.key == "smtp_pass").first()
    if db_pass:
        db_pass.value = encrypted_pass
    else:
        db_pass = Setting(key="smtp_pass", value=encrypted_pass)
        db.add(db_pass)
        
    db.commit()


def fetch_and_store_emails(db: Session):
    """
    Main function for the email job.
    1. Connects to the Gmail API.
    2. Fetches unread emails.
    3. Stores emails in the database (or performs other actions).
    """
    print("Executing email search job...")
    
    try:
        service = get_gmail_service()
        
        # Fetch unread emails
        results = service.users().messages().list(userId='me', q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            print("No unread messages found.")
        else:
            print(f"Found {len(messages)} unread messages.")
            # Here you would process and store the emails
            # For now, we just print the count
    except Exception as e:
        # This will catch errors if Google credentials are not yet set up
        print(f"Could not fetch emails. Have you authenticated with Google? Error: {e}")

    print("Email search job finished.")
