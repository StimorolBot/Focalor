import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

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

SMTP_HOST = ""
SMTP_PORT = ""
EMAIL = ""
PASSWORD = ""
