from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import RedirectResponse

from fastapi_users import models
from fastapi_users.authentication import AuthenticationBackend, Strategy
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel


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
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post("/login", name=f"auth:{backend.name}.login", responses=login_responses, )
    async def login(request: Request, credentials: OAuth2PasswordRequestForm = Depends(),
                    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
                    strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy), ):

        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.LOGIN_BAD_CREDENTIALS, )

        if requires_verification and not user.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.LOGIN_USER_NOT_VERIFIED, )

        response = await backend.login(strategy, user)

        await user_manager.on_after_login(user, request, response)
        return response

    return router
