import uuid
from typing import Optional

from pydantic import EmailStr
from fastapi import Depends, Request, Response, status
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers, exceptions, schemas, models
from fastapi.security import OAuth2PasswordRequestForm

from src.database import get_user_db
from src.config import DB_USER_TOKEN

from src.app.authentication.cookie import auth_backend
from src.background_tasks.send_email import send_email
from src.app.authentication.operations.states import UserStates
from src.app.authentication.operations.user_operation import user as user_operation

from src.app.authentication.models.user import User
from src.app.authentication.models.role import Role
from src.app.authentication.models.news_letter import NewsLetter


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = DB_USER_TOKEN
    verification_token_secret = DB_USER_TOKEN

    async def create(self, user_create: schemas.UC, safe: bool = False, request: Optional[Request] = None, ) -> models.UP:
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["is_verified"] = True

        created_user = await self.user_db.create(user_dict)
        await user_operation.create_table(email=user_dict["email"], tables=[Role, NewsLetter])
        await self.on_after_register(created_user, request)
        return created_user

    async def on_after_register(self, user: User, request: Optional[Request] = None) -> dict:
        send_email(state=UserStates.ON_AFTER_REGISTER, username=user.username)
        return {
            "status": status.HTTP_200_OK,
            "data": "Письмо успешно отправлено",
        }

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> Optional[models.UP]:
        try:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(credentials.password, user.hashed_password)
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def get_by_email(self, user_email: str) -> models.UP:
        match len(user_email.split("@")):
            case 1:
                # добавить функцию для входа по username (такая же как по email)
                user = await self.user_db.get_by_username(user_email)
            case 2:
                user = await self.user_db.get_by_email(user_email)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def on_after_login(self, user: models.UP, request: Optional[Request] = None,
                             response: Optional[Response] = None, ) -> dict:
        return {
            "status": status.HTTP_200_OK,
            "data": f"Пользователь '{user.username}' вошел в систему",
        }

    # добавить token_generate, email в BaseUserManager
    async def reset_password(self, token: str, password: str, token_generate: dict, user_email: EmailStr,
                             request: Optional[Request] = None) -> models.UP:
        user_operation.ttl = token_generate["ttl"]
        user_operation.token = token_generate["token"]
        user_operation.token_request = token

        if await user_operation.verified_token():
            user = await self.get_by_email(user_email)
            updated_user = await self._update(user, {"password": password})
            await self.on_after_reset_password(user, request)

        return updated_user

    async def on_after_reset_password(self, user: models.UP, request: Optional[Request] = None) -> dict:
        return {
            "status": status.HTTP_200_OK,
            "data": f"Пользователь '{user.username}' сменил пароль",
        }


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend], )
current_user = fastapi_users.current_user()
