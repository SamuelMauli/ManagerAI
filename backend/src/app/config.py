from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Carrega as variáveis de ambiente do arquivo .env."""
    DATABASE_URL: str
    GROQ_API_KEY: str
    YOUTRACK_API_TOKEN: str
    YOUTRACK_BASE_URL: str

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding='utf-8')

settings = Settings()
