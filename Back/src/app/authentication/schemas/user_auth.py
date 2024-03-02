import uuid
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated
from pydantic import EmailStr, ConfigDict

from fastapi_users import schemas
from fastapi.param_functions import Form

from core.schemas.check_field import CheckPassword, CheckEmail


# будет отображаться при успешном создании пользователя
class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: str
    username: str
    time: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate, CheckPassword):
    email: Annotated[EmailStr, Form(min_length=8, max_length=40)]
    username: Annotated[str, Form(min_length=8, max_length=40)]
    password: Annotated[str, Form(min_length=8, max_length=20)]
    password_confirm: Annotated[str, Form(min_length=8, max_length=20)]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(schemas.BaseUserUpdate):
    ...


class UserResetPassword(CheckPassword, CheckEmail):
    token: Annotated[str, Form(max_length=6)]

    model_config = ConfigDict(from_attributes=True)
