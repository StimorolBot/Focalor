from datetime import datetime
from fastapi_users import schemas
from fastapi import HTTPException, status

from pydantic import EmailStr
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.app.authentication.models.user import User
from src.app.authentication.models.news_letter import NewsLetter
from src.app.authentication.shemas.user_operations import Operations


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

    async def create_user(self):
        created_user = await self.user_manager.create(user_create=self.user_create, safe=True, request=self.request)
        return schemas.model_validate(self.user_schema, created_user)

    async def ttl_check(self) -> bool:
        if self.ttl >= datetime.utcnow():
            return True
        else:
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                                detail={"code": "TIMEOUT",
                                        "data": "Время ожидания токена истекло"})

    @staticmethod
    async def create_table(email: EmailStr, tables: list):
        async with async_session_maker() as session:
            user_id = select(User.id).where(User.email == email)
            for table in tables:
                stmt = insert(table).values({"user_id": user_id, "email": email})
                await session.execute(stmt)
                await session.commit()

    @staticmethod
    async def subscription_news_letter(email: EmailStr, session: AsyncSession):
        stmt = update(NewsLetter).where(NewsLetter.email == email).values({
            "is_subscription": True,
            "subscription_date": datetime.utcnow()})
        await session.execute(stmt)
        await session.commit()


user = UserOperations()
