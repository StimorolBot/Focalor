import uuid
from typing import Optional

from fastapi import HTTPException, status
from fastapi_users import schemas

from pydantic import EmailStr
from pydantic.functional_validators import model_validator

from typing_extensions import Annotated
from fastapi.param_functions import Form


# будет отображаться при успешном создании пользователя
class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    def __init__(self, email: Annotated[EmailStr, Form()],
                 password: Annotated[str, Form()],
                 is_active: Optional[bool] = True,
                 is_superuser: Optional[bool] = False,
                 is_verified: Optional[bool] = False):
        super().__init__(
            email=email,
            password=password,
            is_active=is_active,
            is_superuser=is_superuser,
            is_verified=is_verified)

    @model_validator(mode='after')
    def check_password(self):
        psd = self.password
        forbidden_symbols = " @!#$%^&*()_-+=/.,:;[]{}"
        if len(psd) <= 6:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Длинна пароля должна быть больше 6 символов")
        elif [symbol for symbol in psd if symbol in forbidden_symbols]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Пароль не должно содержать запрещенных символов:{forbidden_symbols}")
        return psd


class UserUpdate(schemas.BaseUserUpdate):
    pass
