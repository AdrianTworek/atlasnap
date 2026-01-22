from pathlib import Path

from pydantic import Field, PostgresDsn, SecretStr
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
    log_level: str = "INFO"

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/atlasnap", repr=False
    )

    # Auth
    jwt_secret: SecretStr = SecretStr("change_me")
    jwt_lifetime_seconds: int = 3600

    # Google OAuth
    google_client_id: SecretStr
    google_client_secret: SecretStr


settings = Settings()
