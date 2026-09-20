from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import os

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./allamni.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me-in-production"
    jwt_access_minutes: int = 30
    jwt_refresh_days: int = 30
    ai_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    odoo_url: str = ""
    odoo_db: str = ""
    odoo_username: str = ""
    odoo_password: str = ""
    odoo_api_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    cors_allowed_origins: str = "http://localhost:8080"
    environment: str = "production"

    @field_validator('gemini_api_key')
    @classmethod
    def validate_gemini_key(cls, v, info):
        provider = info.data.get('ai_provider', 'gemini')
        env = info.data.get('environment', 'production')
        if provider == 'gemini' and not v and env == 'production':
            raise ValueError(
                "GEMINI_API_KEY is required when AI_PROVIDER=gemini. "
                "Get your key from: https://aistudio.google.com/app/apikey"
            )
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
