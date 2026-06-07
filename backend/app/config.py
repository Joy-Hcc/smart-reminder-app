import logging
import warnings
from pydantic_settings import BaseSettings
from functools import lru_cache

logger = logging.getLogger(__name__)

# 开发环境默认密钥（仅用于本地开发，生产环境必须覆盖）
_DEV_SECRET_KEY = "dev-only-smart-reminder-secret-key-change-in-production"


class Settings(BaseSettings):
    app_name: str = "SmartReminder API"
    debug: bool = True
    database_url: str = "sqlite:///./smart_reminder.db"
    secret_key: str = ""
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "noreply@smartreminder.app"
    qweather_key: str = ""
    cors_origins: str = "*"  # 逗号分隔的允许来源，生产环境设置具体域名

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    if not settings.secret_key:
        if not settings.debug:
            raise RuntimeError("SECRET_KEY must be set in production! Check your .env file.")
        # 开发环境使用默认密钥并警告
        settings.secret_key = _DEV_SECRET_KEY
        logger.warning("Using default SECRET_KEY for development. Set SECRET_KEY in .env for production!")
    return settings
