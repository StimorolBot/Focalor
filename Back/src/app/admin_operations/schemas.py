from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PaginationResponse(BaseModel):
    id: UUID
    username: str
    user_role: int
    email: EmailStr
    time: datetime

    class Config:
        orm_mode = True
