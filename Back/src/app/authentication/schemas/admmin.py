from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class PaginationResponse(BaseModel):
    id: UUID
    username: str
    user_role: int
    email: EmailStr
    time: datetime

    model_config = ConfigDict(from_attributes=True)
