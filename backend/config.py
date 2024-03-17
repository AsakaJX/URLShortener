from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # This is fallback values, config variables are loaded from .env file.
    env_name: str = "FALLBACK"
    base_url: str = "https://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        env_file = "backend/.env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name} environment.")
    return settings