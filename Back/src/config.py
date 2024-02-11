import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from celery import Celery

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

JWT_TOKEN = os.environ.get("JWT_TOKEN")
DB_USER_TOKEN = os.environ.get("DB_USER_TOKEN")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

templates = Jinja2Templates(directory="../front/html/")
celery = Celery('send_email_task', broker='redis://localhost:6379')

SMTP_TOKEN = os.environ.get("SMTP_TOKEN")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")

LIFETIME = os.environ.get("LIFETIME")
