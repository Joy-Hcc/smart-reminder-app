from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "SmartReminder API"
    debug: bool = True
    database_url: str = "sqlite:///./smart_reminder.db"
    secret_key: str = "dev-secret-key-change-in-production"
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "noreply@smartreminder.app"
    qweather_key: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
