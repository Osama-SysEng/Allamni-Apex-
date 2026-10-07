from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import os

class Settings(BaseSettings):
    # NOTE: `environment` must stay above `gemini_api_key`: the validator below
    # reads it from info.data, which only holds already-validated fields.
    environment: str = "production"
    database_url: str = "sqlite+aiosqlite:///./allamni.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 30
    jwt_refresh_days: int = 30
    # Mirrors of the .env.example names (ACCESS_TOKEN_EXPIRE_MINUTES /
    # REFRESH_TOKEN_EXPIRE_DAYS) so every documented var maps to a field.
    # jwt_* remain the canonical knobs used by auth code; keep both in sync
    # when deploying (see .env.example notes).
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    log_level: str = "info"
    sentry_dsn: str = ""
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

    @field_validator('gemini_api_key')
    @classmethod
    def validate_gemini_key(cls, v, info):
        provider = info.data.get('ai_provider', os.getenv('AI_PROVIDER', 'gemini'))
        env = info.data.get('environment', os.getenv('ENVIRONMENT', 'production'))
        if provider == 'gemini' and not v and env == 'production':
            raise ValueError(
                "GEMINI_API_KEY is required when AI_PROVIDER=gemini. "
                "Get your key from: https://aistudio.google.com/app/apikey"
            )
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
