"""Application configuration module."""

import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    VISUAL_DB_SERVER: str
    VISUAL_DB_PORT: int = 5432
    VISUAL_DB_NAME: str
    VISUAL_DB_DRIVER: str
    VISUAL_DB_USER: str
    VISUAL_DB_PASSWORD: str

    API_JWT_SECRET: str = secrets.token_urlsafe(32)
    API_JWT_ACCESS_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    SIGNED_URL_EXPIRE_SECONDS: int = 300
    SIGNED_URL_JWT_SECRET: str = secrets.token_urlsafe(32)

    API_BASE_URL: str = ""

    NETWORK_MOUNT_MAPPINGS: str


settings = Settings()
