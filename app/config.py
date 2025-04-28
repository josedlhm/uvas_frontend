from pydantic_settings import BaseSettings   
from pydantic import PostgresDsn

class Settings(BaseSettings):
    """Central runtime configuration."""
    app_name: str = "app"
    db_url: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
