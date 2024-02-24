from fastapi import Request
from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional, Type
from fastapi_users import schemas

from fastapi_users.manager import BaseUserManager


class Operations(BaseModel):
    user_email: Optional[EmailStr] = None
    ttl: Optional[datetime] = None
    token: Optional[str] = None
    token_request: Optional[str] = None
    user_manager: Optional[Type[BaseUserManager]] = None
    user_create: Optional[Type[schemas.UC]] = None
    user_schema: Optional[Type[schemas.UC]] = None
    request: Optional[Type[Request]] = None

    class Config:
        from_attributes = True
