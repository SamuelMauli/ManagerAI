from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', extra='ignore')

    # Configurações do Banco de Dados
    DATABASE_URL: str
    
    # Configurações de Autenticação do Google
    GOOGLE_API_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_SCOPES: str = (
        'openid,https://www.googleapis.com/auth/userinfo.email,'
        'https://www.googleapis.com/auth/userinfo.profile,'
        'https://www.googleapis.com/auth/gmail.readonly,'
        'https://www.googleapis.com/auth/gmail.send,' # NOVO: Escopo para enviar e-mails
        'https://www.googleapis.com/auth/calendar.readonly,'
        'https://www.googleapis.com/auth/calendar.events,' # NOVO: Escopo para criar/editar eventos do calendário
        'https://www.googleapis.com/auth/drive' # NOVO: Escopo para Drive (leitura/escrita). Ou 'drive.readonly'
    )
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    YOU_TRACK_BASE_URL: str
    YOU_TRACK_TOKEN: str


settings = Settings()