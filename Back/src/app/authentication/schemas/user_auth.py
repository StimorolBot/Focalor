import re
import uuid
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated

from fastapi_users import schemas
from fastapi import HTTPException, status
from fastapi.param_functions import Form

from pydantic import EmailStr, BaseModel, ConfigDict
from pydantic.functional_validators import model_validator

from src.base.response import Response as ResponseSchemas


class CheckPassword(BaseModel):
    password: Annotated[str, Form(min_length=8, max_length=20)]
    password_confirm: Annotated[str, Form(min_length=8, max_length=20)]

    @model_validator(mode='after')
    def check_password(self) -> str:
        psd = self.password
        psd_conf = self.password_confirm

        forbidden_symbols = """ "@!#$%^&*'_-+=/|\.,:;()[]{}"""

        match psd:
            case psd if psd != psd_conf:
                detail = ResponseSchemas(status_code=status.HTTP_400_BAD_REQUEST, data="Пароли не совпадают").model_dump()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

            case psd if [symbol for symbol in psd if symbol in forbidden_symbols]:
                detail = ResponseSchemas(status_code=status.HTTP_400_BAD_REQUEST,
                                         data=f"Пароль не должно содержать запрещенных символов:{forbidden_symbols}").model_dump()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

            case psd if re.findall("[^0-9a-zA-Z_]", psd):
                detail = ResponseSchemas(status_code=status.HTTP_400_BAD_REQUEST, data="Пароль не должен включать кириллицу").model_dump()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

        return psd


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


class UserResetPassword(CheckPassword):
    email: Annotated[EmailStr, Form(min_length=8, max_length=40)]
    token: Annotated[str, Form(max_length=6)]

    model_config = ConfigDict(from_attributes=True)
