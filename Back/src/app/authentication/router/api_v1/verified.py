import json
from typing import TYPE_CHECKING

from core.config import redis
from core.database import get_async_session
from core.schemas.response import Response as ResponseSchemas

from fastapi_users.openapi import OpenAPIResponseType
from fastapi import APIRouter, Depends, HTTPException, status
from src.app.authentication.user_manager import UserManager, get_user_manager

from fastapi_users.router.common import ErrorCode, ErrorModel
from src.app.authentication.schemas.user_auth import UserCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def get_verify_user() -> APIRouter:
    router = APIRouter()

    verify_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.VERIFY_USER_BAD_TOKEN: {
                            "summary": "Неверный токен",
                            "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                        },
                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                            "summary": "Пользователь уже верифицирован",
                            "value": {
                                "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                            },
                        },
                    }
                }
            },
        }
    }

    @router.get("/verified/{token}", name="verify:verify", responses=verify_responses)
    async def verify(token: str, session: "AsyncSession" = Depends(get_async_session),
                     user_manager: UserManager = Depends(get_user_manager)) -> ResponseSchemas:
        user_str = await redis.get(token)

        if user_str is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Токен невалиден")

        user_dict = json.loads(user_str)
        user_create = UserCreate(**user_dict)
        await user_manager.create(user_create=user_create, session=session)

        return ResponseSchemas(status_code=status.HTTP_201_CREATED, data=f"Пользователь {user_dict['username']} создан")

    return router
