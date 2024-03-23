from typing import Type

from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Request, status

from fastapi_users import schemas
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

from core.enum.email_states import EmailStates
from core.operation.convert import add_to_redis
from core.operation.generate_token import get_token
from core.schemas.response import Response as ResponseSchemas
from src.app.authentication.user_manager import get_user_manager, UserManager


def get_register_user(user_create_schema: Type[schemas.UC], ) -> APIRouter:
    router = APIRouter()

    register_response: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "Пользователь с таким адресом электронной почты уже существует",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Проверка пароля не удалась.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Пароль должен состоять минимум из 8 символов",
                                }
                            },
                        },
                    }
                }
            },
        },
    }

    @router.post("/register", name="register:register", responses=register_response)
    async def register(request: Request, user_create: user_create_schema = Depends(user_create_schema),
                       user_manager: UserManager = Depends(get_user_manager), ) -> ResponseSchemas:
        await user_manager.validate_password(user_create.password, user_create)
        existing_user = await user_manager.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            detail = ResponseSchemas(status_code=status.HTTP_400_BAD_REQUEST, data="Пользователь с таким почтой уже существует")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

        token, url = get_token(states=EmailStates.EMAIL_CONFIRM, request=request)
        # перед отправкой в редис хэшировать пароли

        user_dict = {
            "email": user_create.email,
            "username": user_create.username,
            "password": user_create.password,
            "password_confirm": user_create.password_confirm
        }

        await add_to_redis(user_data=user_dict, name=token)
        await user_manager.send_email_confirm(user_create.email, request, url)
        return ResponseSchemas(status_code=status.HTTP_200_OK, data="Для завершения регистрации проверьте свой почтовый ящик")

    return router
