from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Carrega as variáveis do arquivo .env na raiz do projeto
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', extra='ignore')

    # Credenciais do Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_SCOPES: str = (
        'openid,https://www.googleapis.com/auth/userinfo.email,'
        'https://www.googleapis.com/auth/userinfo.profile,'
        'https://www.googleapis.com/auth/gmail.readonly,'
        'https://www.googleapis.com/auth/gmail.send,' # NOVO: Escopo para enviar e-mails
        'https://www.googleapis.com/auth/calendar.readonly,'
        'https://www.googleapis.com/auth/calendar.events,' # NOVO: Escopo para criar/editar eventos do calendário
        'https://www.googleapis.com/auth/drive' # NOVO: Escopo para Drive (leitura/escrita). Ou 'drive.readonly'
    )
    
    # Chave para JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

# Instância única que será usada em toda a aplicação
settings = Settings()