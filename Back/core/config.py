import aioredis
from celery import Celery
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    SMTP_TOKEN: str
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_EMAIL: str

    DB_USER_TOKEN: str
    JWT_TOKEN: str
    EX: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


setting = Settings()
templates = Jinja2Templates(directory="../front/html/")
celery = Celery('send_email_task', broker='redis://localhost:6379')
redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
