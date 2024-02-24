from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    post_id: int
    comment_date: datetime
    username: str
    content: str

    model_config = ConfigDict(from_attributes=True)
