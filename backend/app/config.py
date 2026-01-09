"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Daily Mini Crossword"
    debug: bool = False
    secret_key: str = "change-me-in-production-min-32-characters"

    # Database
    # Render provides DATABASE_URL in postgres:// format, but SQLAlchemy needs postgresql://
    database_url: str = "sqlite:///./crossword.db"

    @field_validator("database_url", mode="before")
    @classmethod
    def fix_postgres_url(cls, v: str) -> str:
        """Convert postgres:// to postgresql:// for SQLAlchemy compatibility."""
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # JWT
    jwt_secret_key: str = "change-me-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Server
    host: str = "0.0.0.0"
    port: int = 8000


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
