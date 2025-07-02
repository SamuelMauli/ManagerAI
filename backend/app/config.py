from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Carrega as variáveis do arquivo .env na raiz do projeto
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', extra='ignore')

    # Credenciais do Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    # Chave para JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

# Instância única que será usada em toda a aplicação
settings = Settings()