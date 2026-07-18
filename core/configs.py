from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import declarative_base

from typing import ClassVar

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str

    # To generate a secure JWT_SECRET, run in Python:
    # import secrets; secrets.token_urlsafe(32)
    JWT_SECRET: str

    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    model_config = SettingsConfigDict(
        env_file= ".env",
        case_sensitive=True,
        extra='ignore'
    )

settings = Settings()
