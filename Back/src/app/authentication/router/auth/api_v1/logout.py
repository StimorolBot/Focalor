from typing import Tuple

from fastapi import APIRouter, Depends, status

from fastapi_users import models
from fastapi_users.authentication import AuthenticationBackend, Authenticator, Strategy
from fastapi_users.openapi import OpenAPIResponseType


def get_logout_user(backend: AuthenticationBackend, authenticator: Authenticator, requires_verification: bool = False, ) -> APIRouter:
    router = APIRouter()
    # получить текущего пользователя
    get_current_user_token = authenticator.current_user_token(active=True, verified=requires_verification)

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post("/logout", name=f"auth:{backend.name}.logout", responses=logout_responses)
    async def logout(user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
                     strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy), ):
        user, token = user_token

        return await backend.logout(strategy, user, token)

    return router
