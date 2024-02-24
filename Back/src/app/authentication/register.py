from typing import Type, Annotated

from fastapi_users import models, schemas
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.manager import BaseUserManager, UserManagerDependency

from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Request, status
from fastapi_users.openapi import OpenAPIResponseType

from src.help_func.generate_token import get_token
from src.app.authentication.operations.states import UserStates
from src.background_tasks.send_email import send_email
from src.app.authentication.operations.user_operation import user


def get_register_user(get_user_manager: UserManagerDependency[models.UP, models.ID], user_schema: Type[schemas.U],
                      user_create_schema: Type[schemas.UC], ) -> APIRouter:
    router = APIRouter()

    register_response: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                              "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    }

    @router.post("/register", name="register:register", responses=register_response)
    async def register(request: Request, user_create: Annotated[user_create_schema, Depends()],  # type: ignore
                       user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager), ):
        await user_manager.validate_password(user_create.password, user_create)

        existing_user = await user_manager.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                        "data": "Пользователь с таким именем/почтой уже существует"})

        token = get_token(states=UserStates.EMAIL_CONFIRM, request=request)
        send_email(state=UserStates.EMAIL_CONFIRM, token=token["token"])

        user.ttl = token["ttl"]
        user.token = token["token"].split("/")[2]
        user.user_email = user_create.email
        user.user_manager = user_manager
        user.user_create = user_create
        user.user_schema = user_schema
        user.request = request

        return {
            "status_code": status.HTTP_200_OK,
            "data": "Для завершения регистрации проверьте свой почтовый ящик"
        }

    return router




"""
@router.post("/register", name="register:register",
                 responses={
                     status.HTTP_400_BAD_REQUEST: {
                         "model": ErrorModel,
                         "content": {
                             "application/json": {
                                 "examples": {
                                     ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                                         "summary": "A user with this email already exists.",
                                         "value": {
                                             "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                                         },
                                     },
                                     ErrorCode.REGISTER_INVALID_PASSWORD: {
                                         "summary": "Password validation failed.",
                                         "value": {
                                             "detail": {
                                                 "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                                 "reason": "Password should be"
                                                           "at least 3 characters",
                                             }
                                         },
                                     },
                                 }
                             }
                         },
                     },
                 },
                 )


"""