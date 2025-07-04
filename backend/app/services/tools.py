# backend/app/services/tools.py

from . import google_calendar, google_drive, youtrack

# Este dicionário mapeia o nome da ferramenta para a função Python real
AVAILABLE_TOOLS = {
    "get_user_events_today": google_calendar.get_user_events_today,
    "search_files_in_drive": google_drive.search_files,
    "get_youtrack_issues": youtrack.get_issues,
}

# Esta é a "documentação" que o Gemini vai ler, agora no formato de dicionário Python correto
# que a API do Google entende. Note os tipos em MAIÚSCULAS.
TOOL_CONFIG = {
    "function_declarations": [
        {
            "name": "get_user_events_today",
            "description": "Busca e retorna os eventos do calendário do usuário para o dia de hoje. Use quando o usuário perguntar sobre sua agenda, compromissos ou calendário de hoje.",
            "parameters": {
                "type": "OBJECT",
                "properties": {}
            }
        },
        {
            "name": "search_files_in_drive",
            "description": "Busca por arquivos no Google Drive do usuário com base em uma query de texto.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "O texto ou nome do arquivo a ser buscado. Ex: 'relatório financeiro', 'apresentacao.pptx'"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_youtrack_issues",
            "description": "Busca issues (tarefas) de um projeto específico no YouTrack. Opcionalmente, pode filtrar por um board.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "project_short_name": {
                        "type": "STRING",
                        "description": "O nome curto (ID) do projeto no YouTrack. Ex: 'VOTOAMS', 'AB2B'"
                    },
                    "board_name": {
                        "type": "STRING",
                        "description": "Opcional. O nome exato do board para filtrar os issues."
                    }
                },
                "required": ["project_short_name"]
            }
        }
    ]
}