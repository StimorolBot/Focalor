from pydantic import BaseModel, ConfigDict


class Response(BaseModel):
    status_code: int
    detail: str

    model_config = ConfigDict(from_attributes=True)
