from typing import Type

from fastapi_users import models, schemas
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users.manager import BaseUserManager, UserManagerDependency

from fastapi import APIRouter, Depends, Request, status

from src.app.background_tasks.send_email import send_email
from src.app.background_tasks.create_user_after_confirm_email import CreateUser


def get_register_user(get_user_manager: UserManagerDependency[models.UP, models.ID], user_schema: Type[schemas.U],
                      user_create_schema: Type[schemas.UC], ) -> APIRouter:
    router = APIRouter()

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
    async def register(request: Request, user_create: user_schema = Depends(user_create_schema),  # type: ignore
                       user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager), ):
        send_email(action="email_confirm", request=request)

        CreateUser.user_manager = user_manager
        CreateUser.request = request
        CreateUser.user_create = user_create
        CreateUser.user_schema = user_schema

    return router
