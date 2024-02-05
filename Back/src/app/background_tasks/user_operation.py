from pydantic import BaseModel

from fastapi import HTTPException, status, Request

from fastapi_users import exceptions, schemas
from fastapi_users.router.common import ErrorCode


class Operations(BaseModel):
    user_manager: str = None
    request: str = None
    user_create: str = None
    user_schema: str = None

    token_request: str = None
    token_render: str = None
    ttl: str = None

    class Config:
        from_attributes = True


class UserOperations(Operations):
    def __init__(self):
        super().__init__()

    #user_manager = None
    #request: Request
    #user_create: str
    #user_schema: str

    ##token_request = None
    #token_render = None
    #ttl = None

    async def verified_token(self):
        if self.token_request is None or self.token_render is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_TOKEN",
                        "data": "Токен невалиден"})

        elif self.token_request == self.token_render:
            return True

    async def create(self):
        try:
            created_user = await self.user_manager.create(self.user_create, safe=True, request=self.request)
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": ErrorCode.REGISTER_USER_ALREADY_EXISTS,
                        "data": "Пользователь с таким именем/почтой уже существует"})

        return schemas.model_validate(self.user_schema, created_user)
