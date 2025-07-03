import os
import google.generativeai as genai
from typing import List
from sqlalchemy.orm import Session
from .. import models, crud
from . import google as google_service

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
        return google_service.get_calendar_events(user, time_min, time_max, max_results)
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
        # Esta função precisa ser criada no google_service
        return google_service.search_drive_files(user, query, max_results)
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
        tools=[get_user_emails, get_calendar_events, search_google_drive]
    )
    
    chat_session = model.start_chat()

    # Passa o user_id para as funções de forma implícita
    # O SDK do Gemini irá preencher os outros argumentos a partir da query do usuário
    tool_config = {'function_calling_config': {'allowed_function_names': [
        'get_user_emails',
        'get_calendar_events',
        'search_google_drive'
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