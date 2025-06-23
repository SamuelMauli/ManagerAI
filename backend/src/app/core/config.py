import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Loads environment variables from the .env file."""
    DATABASE_URL: str
    GROQ_API_KEY: str
    YOUTRACK_API_TOKEN: str
    YOUTRACK_BASE_URL: str
    
    # NEW: Secret key for encrypting sensitive data
    SECRET_KEY: str

    # Configure the location of the .env file
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'),
        env_file_encoding='utf-8'
    )

settings = Settings()