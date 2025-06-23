from apscheduler.schedulers.background import BackgroundScheduler
from ..services.email_service import fetch_and_store_emails
from ..database import SessionLocal

def email_job_wrapper():
    """Wrapper to provide a DB session to the email job."""
    db = SessionLocal()
    try:
        fetch_and_store_emails(db)
    finally:
        db.close()

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")

scheduler.add_job(
    func=email_job_wrapper,
    trigger="interval",
    hours=1,
    id="fetch_emails_job",
    name="Busca e armazena e-mails a cada hora",
    replace_existing=True
)