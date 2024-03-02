from fastapi import APIRouter
from typing import Generic, Optional, Sequence, Type

from fastapi_users.jwt import SecretType
from fastapi_users import models, schemas
from fastapi_users.router import get_users_router
from fastapi_users.manager import UserManagerDependency
from fastapi_users.authentication import AuthenticationBackend, Authenticator

from src.app.authentication.router.auth.api_v1.login import get_login_user
from src.app.authentication.router.auth.api_v1.logout import get_logout_user
from src.app.authentication.router.auth.api_v1.verified import get_verify_user
from src.app.authentication.router.auth.api_v1.register import get_register_user
from src.app.authentication.router.auth.api_v1.reset_passord import get_reset_password_user

try:
    from httpx_oauth.oauth2 import BaseOAuth2

    from fastapi_users.router import get_oauth_router
    from fastapi_users.router.oauth import get_oauth_associate_router
except ModuleNotFoundError:  # pragma: no cover
    BaseOAuth2 = Type  # type: ignore


class FastAPIUsers(Generic[models.UP, models.ID]):
    authenticator: Authenticator

    def __init__(self, get_user_manager: UserManagerDependency[models.UP, models.ID], auth_backends: Sequence[AuthenticationBackend], ):
        self.authenticator = Authenticator(auth_backends, get_user_manager)
        self.get_user_manager = get_user_manager
        self.current_user = self.authenticator.current_user

    @staticmethod
    def get_register_router(user_create_schema: Type[schemas.UC]) -> APIRouter:
        return get_register_user(user_create_schema)

    def get_login_router(self, backend: AuthenticationBackend, requires_verification: bool = False) -> APIRouter:
        return get_login_user(backend, self.get_user_manager, requires_verification, )

    def get_logout_router(self, backend: AuthenticationBackend, requires_verification: bool = False) -> APIRouter:
        return get_logout_user(backend, self.authenticator, requires_verification, )

    @staticmethod
    def get_verify_router(user_create_schema: Type[schemas.UC]) -> APIRouter:
        return get_verify_user(user_create_schema)

    @staticmethod
    def get_reset_password_router() -> APIRouter:
        return get_reset_password_user()

    def get_oauth_router(self, oauth_client: BaseOAuth2, backend: AuthenticationBackend,
                         state_secret: SecretType, redirect_url: Optional[str] = None,
                         associate_by_email: bool = False, is_verified_by_default: bool = False, ) -> APIRouter:
        """
        Return an OAuth router for a given OAuth client and authentication backend.

        :param oauth_client: The HTTPX OAuth client instance.
        :param backend: The authentication backend instance.
        :param state_secret: Secret used to encode the state JWT.
        :param redirect_url: Optional arbitrary redirect URL for the OAuth2 flow.
        If not given, the URL to the callback endpoint will be generated.
        :param associate_by_email: If True, any existing user with the same
        e-mail address will be associated to this user. Defaults to False.
        :param is_verified_by_default: If True, the `is_verified` flag will be
        set to `True` on newly created user. Make sure the OAuth Provider you're
        using does verify the email address before enabling this flag.
        """
        return get_oauth_router(
            oauth_client,
            backend,
            self.get_user_manager,
            state_secret,
            redirect_url,
            associate_by_email,
            is_verified_by_default,
        )

    def get_oauth_associate_router(self, oauth_client: BaseOAuth2, user_schema: Type[schemas.U],
                                   state_secret: SecretType, redirect_url: Optional[str] = None,
                                   requires_verification: bool = False, ) -> APIRouter:
        """
        Return an OAuth association router for a given OAuth client.

        :param oauth_client: The HTTPX OAuth client instance.
        :param user_schema: Pydantic schema of a public user.
        :param state_secret: Secret used to encode the state JWT.
        :param redirect_url: Optional arbitrary redirect URL for the OAuth2 flow.
        If not given, the URL to the callback endpoint will be generated.
        :param requires_verification: Whether the endpoints
        require the users to be verified or not. Defaults to False.
        """
        return get_oauth_associate_router(
            oauth_client,
            self.authenticator,
            self.get_user_manager,
            user_schema,
            state_secret,
            redirect_url,
            requires_verification,
        )

    def get_users_router(self, user_schema: Type[schemas.U], user_update_schema: Type[schemas.UU],
                         requires_verification: bool = False, ) -> APIRouter:
        """
        Return a router with routes to manage users.

        :param user_schema: Pydantic schema of a public user.
        :param user_update_schema: Pydantic schema for updating a user.
        :param requires_verification: Whether the endpoints
        require the users to be verified or not. Defaults to False.
        """
        return get_users_router(
            self.get_user_manager,
            user_schema,
            user_update_schema,
            self.authenticator,
            requires_verification,
        )
