from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_users import models
from fastapi_users.authentication import AuthenticationBackend, Strategy
from fastapi_users.manager import UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

if TYPE_CHECKING:
    from src.app.authentication.user_manager import UserManager


def get_login_user(backend: AuthenticationBackend, get_user_manager: UserManagerDependency[models.UP, models.ID],
                   requires_verification: bool = False, ) -> APIRouter:
    router = APIRouter()

    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Неверный логин/пароль",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post("/login", name=f"auth:{backend.name}.login", responses=login_responses)
    async def login(credentials: OAuth2PasswordRequestForm = Depends(),
                    user_manager: "UserManager" = Depends(get_user_manager),
                    strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy), ):

        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.LOGIN_BAD_CREDENTIALS, )

        if requires_verification and not user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.LOGIN_USER_NOT_VERIFIED, )

        await user_manager.on_after_login(user)
        return await backend.login(strategy, user)

    return router
