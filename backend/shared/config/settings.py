from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./allamni.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me"
    jwt_access_minutes: int = 30
    jwt_refresh_days: int = 30
    llm_provider: str = "mock"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    odoo_url: str = ""
    odoo_db: str = ""
    odoo_username: str = ""
    odoo_api_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    cors_allowed_origins: str = "http://localhost:8080"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
