from typing import Optional, Type, Dict, Any, List, Union
from pydantic import BaseModel, ConfigDict
from fastapi.templating import Jinja2Templates


# request: Optional[Type[Request]] = None

class Response(BaseModel):
    status_code: int
    detail: str

    model_config = ConfigDict(from_attributes=True)
