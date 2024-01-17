import uuid
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions, schemas, models
from fastapi.security import OAuth2PasswordRequestForm

from src.config import DB_USER_TOKEN
from src.app.authentication.models import User
from src.database import get_user_db
from src.app.authentication.background_tasks.send_email import send_email_after_register


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = DB_USER_TOKEN
    verification_token_secret = DB_USER_TOKEN

    async def create(self, user_create: schemas.UC, safe: bool = False, request: Optional[Request] = None, ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["user_role"] = 2

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(self, user: User, request: Optional[Request] = None) -> dict:
        send_email_after_register.delay(username=user.username)
        return {
            "status": 201,
            "data": "Письмо отправлено",
            "details": None
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
                user = await self.user_db.get_by_username(user_email)
            case 2:
                user = await self.user_db.get_by_email(user_email)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def on_after_login(self, user: models.UP, request: Optional[Request] = None, response: Optional[Response] = None, ):
        print(f"{user.email} вошел в систему")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
