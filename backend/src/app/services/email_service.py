from sqlalchemy.orm import Session
from ..models.setting import Setting
from ..core.security import encrypt_data, decrypt_data
from ..schemas.setting import EmailConfig

def get_email_config(db: Session) -> dict:
    """Retrieves email configuration from the database."""
    email_entry = db.query(Setting).filter(Setting.key == "email_address").first()
    creds_entry = db.query(Setting).filter(Setting.key == "email_credentials").first()
    
    if not email_entry or not creds_entry:
        return {}
        
    return {
        "email": email_entry.value,
        "credentials": decrypt_data(creds_entry.value)
    }

def update_email_config(db: Session, config: EmailConfig):
    """Updates or creates email configuration in the database."""
    # Email Address
    email_entry = db.query(Setting).filter(Setting.key == "email_address").first()
    if email_entry:
        email_entry.value = config.email
    else:
        email_entry = Setting(key="email_address", value=config.email)
        db.add(email_entry)

    # Encrypted Credentials
    creds_entry = db.query(Setting).filter(Setting.key == "email_credentials").first()
    encrypted_creds = encrypt_data(config.credentials)
    if creds_entry:
        creds_entry.value = encrypted_creds
    else:
        creds_entry = Setting(key="email_credentials", value=encrypted_creds)
        db.add(creds_entry)
    
    db.commit()
    db.refresh(email_entry)
    db.refresh(creds_entry)
    return {"message": "Email configuration updated successfully."}


def fetch_and_store_emails(db: Session):
    """
    Main function for the email job.
    1. Gets config from the DB.
    2. Connects to the Gmail API (placeholder).
    3. Fetches unread emails.
    4. Stores emails in the database.
    """
    print("Executing email search job...")
    
    config = get_email_config(db)
    if not config:
        print("Email configuration not found. Skipping job.")
        return

    print(f"Connecting to Gmail for user: {config['email']}...")
    
    # --- GMAIL API CONNECTION LOGIC GOES HERE ---
    # This is where you would use google-api-python-client
    # to connect, authenticate, and fetch emails.
    # For now, it remains a placeholder.
    #
    # Example placeholder logic:
    # 1. Authenticate using stored credentials.
    # 2. Search for emails (e.g., is:unread).
    # 3. For each email found:
    #    email_data = {
    #        "message_id": "unique_id",
    #        "sender": "sender@example.com",
    #        "subject": "Email Subject",
    #        "body": "This is the email body.",
    #        "received_at": datetime.now()
    #    }
    #    new_email = Email(**email_data)
    #    db.add(new_email)
    #    db.commit()
    
    print("Email search job finished.")