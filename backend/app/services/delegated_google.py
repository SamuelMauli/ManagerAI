from .auth import create_service # Importando a função do seu PDF

def get_user_calendar_events(user_email: str):
    """
    Busca eventos do calendário para um usuário específico usando DWD.
    """
    try:
        # Escopo necessário para ler o calendário
        scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        # Cria o serviço autenticado personificando o usuário
        service = create_service(user_email, 'calendar', 'v3', *scopes)

        # Agora você pode usar o 'service' para chamar a API do Google Calendar
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        return events

    except Exception as e:
        print(f"Erro ao acessar o calendário para {user_email}: {e}")
        return None