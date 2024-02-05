import aioredis
from fastapi import FastAPI, Request

from fastapi_cache import FastAPICache
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from starlette.exceptions import HTTPException

from src.config import templates
from src.router.router_admin import router_admin
from src.router.router_user import router_user

from src.app.authentication.user_manager import get_user_manager
from src.app.authentication.cookie import auth_backend
from src.app.authentication.schemas import UserRead, UserCreate
from src.app.authentication.models import User
from src.app.authentication.fastapi_users_custom import FastAPIUsers

app = FastAPI(title="main_app")

# добавление пагинации страниц
add_pagination(app)

# подключение роутеров
app.include_router(router_user)
app.include_router(router_admin)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend], )

app.include_router(fastapi_users.get_login_router(auth_backend), tags=["auth"], )
app.include_router(fastapi_users.get_logout_router(auth_backend), tags=["auth"], )
app.include_router(fastapi_users.get_register_user(UserRead, UserCreate), tags=["auth"], )
app.include_router(fastapi_users.get_reset_password_router(), tags=["auth"],)

# подключать в самом конце, иначе выдает ошибку "Метод не разрешен"
app.mount("/", StaticFiles(directory="../Front/"), name="css", )  # подключение css, js и img

# адреса, имеющие доступ к бэку
origins = [
    "http://localhost:8000",
]

# http://127.0.0.1:8000/docs документация
# uvicorn src.main:app --reload - запуск сервера
# celery -A src.app.background_tasks.send_email:celery worker --loglevel=INFO --pool=solo
# - запуск celery (перезагружать после изменения кода) (прописывать путь туда, где вещается task)
# celery -A src.config:celery flower - запуск веб интерфейса
# http://localhost:5555/ интерфейс


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],  # разрешенные методы
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "status_code": exc.status_code,
        "title": f"Error {exc.status_code}",
        "error_details": exc.detail["data"]
    })


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
