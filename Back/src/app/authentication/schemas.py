import uuid
from typing import Optional

from fastapi_users import schemas
from fastapi import HTTPException, status
from fastapi.param_functions import Form
from fastapi_users.router.common import ErrorCode

from pydantic import EmailStr
from pydantic.functional_validators import model_validator

from datetime import datetime
from typing_extensions import Annotated


# будет отображаться при успешном создании пользователя
class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: str
    username: str
    time: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


# чтобы не было ошибки добавил в BaseUserCreate username
class UserCreate(schemas.BaseUserCreate):
    def __init__(self, email: Annotated[EmailStr, Form()],
                 username: Annotated[str, Form()],
                 password: Annotated[str, Form()],
                 is_active: Optional[bool] = True,
                 is_superuser: Optional[bool] = False,
                 is_verified: Optional[bool] = False):
        super().__init__(
            email=email,
            username=username,
            password=password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified)

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_password(self):
        psd = self.password
        forbidden_symbols = " @!#$%^&*()_-+=/.,:;[]{}"
        if len(psd) <= 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": ErrorCode.REGISTER_INVALID_PASSWORD,
                        "data": "Длинна пароля должна быть больше 6 символов"})

        elif [symbol for symbol in psd if symbol in forbidden_symbols]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": ErrorCode.REGISTER_INVALID_PASSWORD,
                        "data": f"Пароль не должно содержать запрещенных символов:{forbidden_symbols}"})
        return psd


class UserUpdate(schemas.BaseUserUpdate):
    pass
