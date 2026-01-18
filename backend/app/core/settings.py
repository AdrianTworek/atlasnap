from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Atlasnap API"
    version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@db:5432/atlasnap"
    )


settings = Settings()
