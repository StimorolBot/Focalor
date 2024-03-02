import asyncio
import uvicorn
from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend

from starlette.exceptions import HTTPException

from core.logger.logger import logger
from core.config import templates, redis

from src.app.authentication.router.users.api_v1 import router
from src.app.authentication.router.auth.api_v1 import router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="auth_app", lifespan=lifespan)

# добавление пагинации страниц
add_pagination(app)

# подключение роутеров
app.include_router(router)
app.include_router(router_auth)

# подключать в самом конце, иначе выдает ошибку "Метод не разрешен"
app.mount("/", StaticFiles(directory="../Front/"), name="css", )  # подключение css, js и img

# адреса, имеющие доступ к бэку
origins = ["http://localhost:8000", ]

# http://127.0.0.1:8000/docs документация
# uvicorn src.main:app --reload - запуск сервера
# celery -A src.background_tasks.send_email:celery worker --loglevel=INFO --pool=solo
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


@app.middleware("http")
async def check_server_error(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except (OSError, TypeError, AttributeError) as error:
        logger.error(error)
        return templates.TemplateResponse("error.html", {
            "request": request,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "title": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error_details": "Внутренняя ошибка сервера"
        })


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exc: HTTPException) -> templates.TemplateResponse:
    if isinstance(exc.detail, str):
        exc.detail = {"data": exc.detail}

    return templates.TemplateResponse("error.html", {
        "request": request,
        "status_code": exc.status_code,
        "title": f"Error {exc.status_code}",
        "error_details": exc.detail["data"]
    })


async def main():
    config = uvicorn.Config(app="main:app", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


# нежно перезагружать после изменения кода, поэтому лучше запускать через терминал
if __name__ == '__main__':
    asyncio.run(main())
