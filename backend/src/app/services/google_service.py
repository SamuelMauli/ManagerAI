import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# AJUSTE: Caminho para o arquivo JSON da conta de serviço
# Este arquivo deve ser colocado na raiz do backend e o caminho
# deve ser definido em uma variável de ambiente.
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_account.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    """
    Cria e retorna um serviço do Gmail autenticado usando uma conta de serviço.
    """
    creds = None
    try:
        # Carrega as credenciais a partir do arquivo da conta de serviço
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        
        # Você precisa delegar autoridade de todo o domínio para a conta de serviço
        # no seu Google Workspace Admin Console para que ela possa personificar um usuário.
        # Substitua 'user@yourdomain.com' pelo e-mail do usuário que você quer personificar.
        delegated_creds = creds.with_subject(os.getenv("GMAIL_USER_EMAIL"))
        
        service = build("gmail", "v1", credentials=delegated_creds)
        logging.info("Serviço do Gmail autenticado com sucesso.")
        return service

    except FileNotFoundError:
        logging.error(f"Erro: O arquivo de credenciais '{SERVICE_ACCOUNT_FILE}' não foi encontrado.")
        logging.error("Certifique-se de que o arquivo JSON da conta de serviço está no local correto e a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS está definida.")
        return None
    except Exception as e:
        logging.error(f"Ocorreu um erro ao criar o serviço do Gmail: {e}")
        return None

# Função para buscar e-mails (exemplo de uso do serviço)
def fetch_emails():
    service = get_gmail_service()
    if not service:
        return []
    
    try:
        results = service.users().messages().list(userId="me", maxResults=5).execute()
        messages = results.get("messages", [])
        
        email_list = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            email_list.append(msg_data)
            
        return email_list
        
    except HttpError as error:
        logging.error(f"Ocorreu um erro HTTP ao buscar e-mails: {error}")
        return []