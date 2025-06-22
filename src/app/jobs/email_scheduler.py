from apscheduler.schedulers.background import BackgroundScheduler
from ..services.email_service import fetch_and_store_emails

scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")

scheduler.add_job(
    func=fetch_and_store_emails, 
    trigger="interval", 
    hours=1,
    id="fetch_emails_job",
    name="Busca e armazena e-mails a cada hora",
    replace_existing=True
)
