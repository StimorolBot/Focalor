import uuid
from pydantic import EmailStr
from typing import TYPE_CHECKING, Optional

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers, models, exceptions

from src.background_tasks.send_email import send_email
from src.app.authentication.cookie import auth_backend
from src.app.authentication.models.user import User
from src.app.authentication.models.role import Role
from src.app.authentication.models.news_letter import NewsLetter
from src.app.authentication.operations.user_operation import user as user_operation

from core.config import setting
from core.operation.crud import Crud
from core.logger.logger import logger
from core.database import get_user_db
from core.models.logger import LoggerResponse
from core.enum.email_states import EmailStates
from core.enum.logger_states import LoggerStates, LoggerDetail

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from fastapi.security import OAuth2PasswordRequestForm
    from src.app.authentication.schemas.user_auth import UserCreate
    from src.app.authentication.schemas.user_auth import UserResetPassword


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = setting.DB_USER_TOKEN
    verification_token_secret = setting.DB_USER_TOKEN

    async def create(self, user_create: "UserCreate", session: "AsyncSession", safe: bool = False) -> models.UP:
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        user_dict.__delitem__("password_confirm")
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["is_verified"] = True

        created_user = await self.user_db.create(user_dict)
        await user_operation.add_role_and_newsletter(email=user_dict["email"], tables=[Role, NewsLetter], session=session)
        await self.on_after_register(created_user)
        return created_user

    @classmethod
    async def get_by_login(cls, login: str, session: "AsyncSession") -> models.UP:
        user = None
        match login:
            case login if "@" in login:
                user = await Crud.read_one(session=session,table=User, table_field=User.email, login=login)

            case login if "@" not in login:
                user = await Crud.read_one(session=session,table=User, table_field=User.username, login=login)

        if user is None:
            raise exceptions.UserNotExists()
        return user

    async def authenticate_custom(self, credentials: "OAuth2PasswordRequestForm", session: "AsyncSession") -> Optional[models.UP]:
        try:
            user = await self.get_by_login(credentials.username, session)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(credentials.password, user.hashed_password)
        if not verified:
            return None

        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    @staticmethod
    async def send_email_confirm(user_email: EmailStr, token: str):
        send_email(state=EmailStates.EMAIL_CONFIRM, token=token)
        log_msg = LoggerResponse(state=LoggerStates.REQUEST.value, detail=LoggerDetail.MAIL_CONFIRMATION.value, user_data=user_email)
        logger.info(msg=log_msg.msg)

    @staticmethod
    async def on_after_register(user: "User"):
        send_email(state=EmailStates.ON_AFTER_REGISTER, username=user.username)
        log_msg = LoggerResponse(state=LoggerStates.OK.value, detail=LoggerDetail.MAIL_CONFIRM.value, user_data=user.email)
        logger.info(msg=log_msg.msg)

    @staticmethod
    async def on_after_login(user: "User"):
        log_msg = LoggerResponse(state=LoggerStates.OK.value, detail=LoggerDetail.LOGIN.value, user_data=user.email)
        logger.info(msg=log_msg.msg)

    @staticmethod
    async def on_after_logout(user: "User"):
        log_msg = LoggerResponse(state=LoggerStates.OK.value, detail=LoggerDetail.LOGOUT.value, user_data=user.email)
        logger.info(msg=log_msg.msg)

    @staticmethod
    async def on_after_subscribe(email: "EmailStr"):
        log_msg = LoggerResponse(state=LoggerStates.OK.value, detail=LoggerDetail.SUBSCRIBE_ON_NEWSLETTER.value, user_data=email)
        logger.info(msg=log_msg.msg)

    @staticmethod
    async def on_after_reset_password(user: "UserResetPassword"):
        send_email(state=EmailStates.ON_AFTER_RESET_PASSWORD, username=user.username)
        log_msg = LoggerResponse(state=LoggerStates.OK.value, detail=LoggerDetail.RESET_PASSWORD.value, user_data=user.email)
        logger.info(msg=log_msg.msg)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend], )
current_user = fastapi_users.current_user()
