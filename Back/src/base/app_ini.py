from src.main import app_auth

from fastapi import FastAPI, Request

from fastapi_cache import FastAPICache
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException

from src.config import templates
from src.router.router_admin import router_admin
from src.router.router_user import router_user

from src.app.authentication.user_manager import get_user_manager
from src.app.authentication.cookie import auth_backend
from src.app.authentication.schemas.user_auth import UserRead, UserCreate
from src.app.authentication.models.user import User
from src.app.authentication.fastapi_users_custom import FastAPIUsers

# подключение роутеров
app_auth.include_router(router_user)
app_auth.include_router(router_admin)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend], )

app_auth.include_router(fastapi_users.get_login_router(auth_backend), tags=["auth"], )
app_auth.include_router(fastapi_users.get_logout_router(auth_backend), tags=["auth"], )
app_auth.include_router(fastapi_users.get_register_user(UserRead, UserCreate), tags=["auth"], )
app_auth.include_router(fastapi_users.get_reset_password_router(), tags=["auth"], )

# добавление пагинации страниц
add_pagination(app_auth)

# подключать в самом конце, иначе выдает ошибку "Метод не разрешен"
app_auth.mount("/", StaticFiles(directory="../Front/"), name="css", )  # подключение css, js и img

origins = [
    "http://localhost:8000",
]

app_auth.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],  # разрешенные методы
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)


@app_auth.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "status_code": exc.status_code,
            "title": f"Error {exc.status_code}",
            "error_details": exc.detail["data"]
        })
    return templates.TemplateResponse("error.html", {
        "request": request,
        "status_code": exc.status_code,
        "title": f"Error {exc.status_code}",
        "error_details": exc.detail
    })