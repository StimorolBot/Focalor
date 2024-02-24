from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    user_id: UUID
    comment: str

    model_config = ConfigDict(from_attributes=True)
