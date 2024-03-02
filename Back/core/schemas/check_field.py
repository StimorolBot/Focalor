import re
from typing_extensions import Annotated
from fastapi.param_functions import Form
from pydantic import EmailStr, BaseModel

from fastapi import HTTPException, status
from pydantic.functional_validators import model_validator
from core.schemas.response import Response as ResponseSchemas


class CheckEmail(BaseModel):
    email: Annotated[EmailStr, Form(min_length=8, max_length=40)]

    @model_validator(mode='after')
    def check_email(self) -> EmailStr:
        user_email = self.email

        return user_email


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
