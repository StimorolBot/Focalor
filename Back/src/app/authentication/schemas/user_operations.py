from fastapi import Request
from fastapi_users import schemas
from fastapi_users.manager import BaseUserManager

from datetime import datetime
from typing import Optional, Type
from pydantic import BaseModel, EmailStr, ConfigDict


class Operations(BaseModel):
    user_email: Optional[EmailStr] = None
    ttl: Optional[datetime] = None
    token: Optional[str] = None
    user_manager: Optional[Type[BaseUserManager]] = None
    user_create: Optional[Type[schemas.UC]] = None
    user_schema: Optional[Type[schemas.UC]] = None
    request: Optional[Type[Request]] = None

    model_config = ConfigDict(from_attributes=True)
