import os
import google.generativeai as genai
from typing import List
from sqlalchemy.orm import Session
from .. import models, crud
from . import google as google_service
from ..schemas import DriveFileContent # Importar o schema de conteúdo de arquivo

# Configura a API do Gemini
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    print("Google API Key configured successfully.")
except Exception as e:
    print(f"Failed to configure Google API Key: {e}")

# --- Ferramentas que o Gemini pode usar ---

def get_user_emails(user_id: int, query: str = None, unread_only: bool = False, max_results: int = 10):
    """
    Busca os e-mails de um usuário no banco de dados.

    Args:
        user_id: O ID do usuário.
        query: Um termo para buscar no assunto ou corpo do e-mail.
        unread_only: Se verdadeiro, busca apenas e-mails não lidos.
        max_results: Número máximo de e-mails para retornar.
    """
    from ..database import SessionLocal
    db: Session = SessionLocal()
    try:
        if unread_only:
            emails = crud.get_unread_emails_by_user(db, user_id=user_id, limit=max_results)
        else:
            # Esta função precisaria ser implementada no crud.py para buscar com query
            # Por simplicidade, vamos usar a função existente.
            # Para buscar por query no conteúdo, você precisaria estender crud.get_emails_by_user
            # para aceitar um parâmetro 'query' e filtrar o assunto/corpo.
            emails = crud.get_emails_by_user(db, user_id=user_id, limit=max_results)

        return [
            {
                "from": email.sender,
                "subject": email.subject,
                "snippet": email.snippet,
                "received_at": email.received_at.isoformat(),
                "is_read": email.is_read
            } for email in emails
        ]
    finally:
        db.close()


def get_calendar_events(user_id: int, time_min: str = None, time_max: str = None, max_results: int = 10):
    """
    Busca os eventos da agenda do usuário no Google Calendar.

    Args:
        user_id: O ID do usuário.
        time_min: Data e hora de início no formato ISO (ex: 2024-07-25T00:00:00Z). Padrão: início do dia de hoje.
        time_max: Data e hora de fim no formato ISO (ex: 2024-07-25T23:59:59Z). Padrão: fim do dia de hoje.
        max_results: Número máximo de eventos para retornar.
    """
    from ..database import SessionLocal
    db: Session = SessionLocal()
    try:
        user = crud.get_user(db, user_id)
        if not user or not user.access_token:
            return "Usuário não autenticado com o Google."
        return google_service.get_events_for_today(db, user) # Usando get_events_for_today que já filtra por hoje
    finally:
        db.close()

def create_calendar_event_tool(user_id: int, summary: str, start_time: str, end_time: str, description: str = None, attendees: List[str] = None):
    """
    Cria um novo evento no Google Calendar do usuário.

    Args:
        user_id: O ID do usuário.
        summary: Título do evento.
        start_time: Data e hora de início no formato ISO (ex: 2024-07-25T09:00:00Z).
        end_time: Data e hora de fim no formato ISO (ex: 2024-07-25T10:00:00Z).
        description: Descrição do evento (opcional).
        attendees: Lista de e-mails dos participantes (opcional).
    """
    from ..database import SessionLocal
    db: Session = SessionLocal()
    try:
        user = crud.get_user(db, user_id)
        if not user or not user.access_token:
            return "Usuário não autenticado com o Google."
        
        event_data = schemas.CalendarEventCreate(
            summary=summary,
            description=description,
            start_time=datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00')),
            end_time=datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00')),
            attendees=attendees
        )
        created_event = google_service.create_calendar_event(db, user, event_data)
        return f"Evento '{created_event.get('summary')}' criado com sucesso no calendário com ID: {created_event.get('id')}"
    except Exception as e:
        return f"Erro ao criar evento no calendário: {e}"
    finally:
        db.close()


def search_google_drive(user_id: int, query: str, max_results: int = 10):
    """
    Busca arquivos no Google Drive do usuário.

    Args:
        user_id: O ID do usuário.
        query: O termo de busca para os nomes dos arquivos.
        max_results: Número máximo de arquivos para retornar.
    """
    from ..database import SessionLocal
    db: Session = SessionLocal()
    try:
        user = crud.get_user(db, user_id)
        if not user or not user.access_token:
            return "Usuário não autenticado com o Google."
        return google_service.search_drive_files(user, query, max_results)
    finally:
        db.close()

def get_drive_file_content_tool(user_id: int, file_id: str):
    """
    Obtém o conteúdo textual de um arquivo específico do Google Drive.
    Esta ferramenta é útil para que o modelo Gemini possa 'ler' o conteúdo de documentos.

    Args:
        user_id: O ID do usuário.
        file_id: O ID do arquivo no Google Drive.
    """
    from ..database import SessionLocal
    db: Session = SessionLocal()
    try:
        user = crud.get_user(db, user_id)
        if not user or not user.access_token:
            return "Usuário não autenticado com o Google."
        
        file_content_obj = google_service.get_drive_file_content(db, user, file_id)
        if file_content_obj and file_content_obj.content:
            return f"Conteúdo do arquivo '{file_content_obj.file_name}' (Tipo: {file_content_obj.mime_type}):\n\n{file_content_obj.content[:2000]}..." # Limita o conteúdo para evitar excesso de tokens
        else:
            return f"Não foi possível obter o conteúdo do arquivo com ID {file_id}. Pode não ser um arquivo de texto ou o conteúdo é muito grande/não suportado para leitura direta."
    except Exception as e:
        return f"Erro ao tentar obter o conteúdo do arquivo do Drive: {e}"
    finally:
        db.close()

def send_email_tool(user_id: int, to: str, subject: str, body: str, is_html: bool = False, in_reply_to_id: str = None, thread_id: str = None):
    """
    Envia um e-mail para um destinatário específico em nome do usuário.

    Args:
        user_id: O ID do usuário.
        to: Endereço de e-mail do destinatário.
        subject: Assunto do e-mail.
        body: Corpo do e-mail.
        is_html: Se o corpo do e-mail é HTML (True) ou texto simples (False).
        in_reply_to_id: ID da mensagem à qual este e-mail está respondendo (opcional).
        thread_id: ID da conversa a qual este e-mail pertence (opcional).
    """
    from ..database import SessionLocal
    db: Session = SessionLocal()
    try:
        user = crud.get_user(db, user_id)
        if not user or not user.access_token:
            return "Usuário não autenticado com o Google para enviar e-mails."
        
        email_data = schemas.EmailSendRequest(
            to=to,
            subject=subject,
            body=body,
            is_html=is_html,
            in_reply_to_id=in_reply_to_id,
            thread_id=thread_id
        )
        sent_message = google_service.send_email(db, user, email_data)
        return f"E-mail enviado com sucesso para {to} com o assunto '{subject}'. ID da mensagem: {sent_message.get('id')}"
    except Exception as e:
        return f"Erro ao enviar e-mail: {e}"
    finally:
        db.close()

# --- Orquestrador Principal do Chat ---

def generate_chat_response(query: str, user: models.User) -> str:
    """
    Gera uma resposta de chat usando o Gemini e as ferramentas disponíveis.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        return "A API do Gemini não está configurada no servidor."

    # Define o modelo com as ferramentas
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', # Usando um modelo rápido e eficiente
        tools=[get_user_emails, get_calendar_events, search_google_drive, create_calendar_event_tool, get_drive_file_content_tool, send_email_tool] # Adicionar novas ferramentas
    )
    
    chat_session = model.start_chat()

    # Passa o user_id para as funções de forma implícita
    # O SDK do Gemini irá preencher os outros argumentos a partir da query do usuário
    tool_config = {'function_calling_config': {'allowed_function_names': [
        'get_user_emails',
        'get_calendar_events',
        'search_google_drive',
        'create_calendar_event_tool', # Adicionar
        'get_drive_file_content_tool', # Adicionar
        'send_email_tool' # Adicionar
    ]}}
    
    prompt = f"O ID do usuário é {user.id}. Responda à seguinte pergunta: {query}"

    try:
        # Envia a query para o modelo
        response = chat_session.send_message(prompt, tool_config=tool_config)
        
        # Loop para lidar com chamadas de função (ferramentas)
        while response.function_calls:
            api_requests_and_responses = []
            for function_call in response.function_calls:
                # Chama a função Python correspondente
                function_to_call = globals()[function_call.name]
                
                # Prepara os argumentos, garantindo que o user_id está presente
                args = dict(function_call.args)
                args['user_id'] = user.id

                function_response = function_to_call(**args)
                
                # Coleta a resposta para enviar de volta ao modelo
                api_requests_and_responses.append({
                    "function_call": function_call,
                    "response": {"name": function_call.name, "content": function_response}
                })

            # Envia o resultado da ferramenta de volta para o modelo
            response = chat_session.send_message(api_requests_and_responses)

        return response.text

    except Exception as e:
        print(f"Erro ao gerar resposta do Gemini: {e}")
        return "Desculpe, não consegui processar sua solicitação no momento."