from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ServerResponse(BaseModel):
    id: UUID
    username: str | None
    user_role: int
    email: EmailStr
    time: datetime

    class Config:
        orm_mode = True
