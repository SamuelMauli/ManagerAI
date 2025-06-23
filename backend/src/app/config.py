from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ManagerAI Backend"

    # Database
    DATABASE_URL: str
    
    # APIs & Secrets
    GROQ_API_KEY: str
    YOUTRACK_API_TOKEN: str
    YOUTRACK_BASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

settings = Settings()
