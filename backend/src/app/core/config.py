from typing import Optional
from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ManagerAI"
    API_V1_STR: str = "/api"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 
    DATABASE_URL: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    GROQ_API_KEY: str

    # Credenciais do YouTrack carregadas do ambiente
    YOUTRACK_BASE_URL: str
    YOUTRACK_API_TOKEN: str

    class Config:
        case_sensitive = True
        env_file = ".env"  # Mesmo que não usemos, é boa prática manter
        env_file_encoding = "utf-8"

settings = Settings()