from datetime import datetime
from fastapi_users import schemas
from fastapi import HTTPException, status
from src.operations.user.schemas import Operations


class UserOperations(Operations):
    def __init__(self):
        super().__init__()

    async def verified_token(self):
        if self.token_request is None or self.token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_TOKEN",
                        "data": "Токен невалиден"})

        elif (self.token_request == self.token) and await self.ttl_check() is True:
            return True

    async def create(self):
        created_user = await self.user_manager.create(user_create=self.user_create, safe=True, request=self.request)
        return schemas.model_validate(self.user_schema, created_user)

    async def ttl_check(self) -> bool:
        if self.ttl >= datetime.utcnow():
            return True
        else:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                detail={"code": "TIMEOUT",
                                        "data": "Время ожидания токена истекло"})


user = UserOperations()
