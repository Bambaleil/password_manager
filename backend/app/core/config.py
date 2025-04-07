import secrets
from pathlib import Path

from cryptography.fernet import Fernet
from pydantic import PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = ""
    HOST_BACKEND: str = ""
    PORT_BACKEND: int = 8000

    SECRET_KEY: str = secrets.token_urlsafe(32)
    FERNET_KEY: str = Fernet.generate_key().decode()
    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    DB_ECHO: bool = False

    REDIS_SERVER: str = ""
    REDIS_PORT: int = 6380
    REDIS_PASSWORD: str = ""
    REDIS_USER: str = ""
    REDIS_USER_PASSWORD: str = ""

    REDIS_CACHE_DB: str = ""
    REDIS_CELERY_DB: str = ""

    CELERY_TTL: int = 120

    @computed_field  # type: ignore
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore
    @property
    def REDIS_CACHE_URI(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USER,
            password=self.REDIS_USER_PASSWORD,
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_CACHE_DB}",
        )

    @computed_field  # type: ignore
    @property
    def REDIS_CELERY_URI(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USER,
            password=self.REDIS_USER_PASSWORD,
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_CELERY_DB}",
        )

    FIRST_SUPERUSER: str = ""
    FIRST_SUPERUSER_PASSWORD: str = ""


settings: Settings = Settings()
