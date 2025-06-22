# src/app/services/email_service.py
from ..database import SessionLocal

def fetch_and_store_emails():
    """
    Função principal do job de e-mails.
    1. Conecta-se à API do Gmail.
    2. Busca e-mails não lidos ou desde a última verificação.
    3. Para cada e-mail, extrai as informações.
    4. Salva o e-mail no banco de dados.
    """
    db = SessionLocal()
    try:
        print("Executando job de busca de e-mails...")
        # LÓGICA DE CONEXÃO COM GMAIL API AQUI
        # ... buscar e-mails ...
        # email_data = {"message_id": "...", "sender": "...", ...}
        # new_email = Email(**email_data)
        # db.add(new_email)
        # db.commit()
        print("Job de busca de e-mails finalizado.")
    finally:
        db.close()