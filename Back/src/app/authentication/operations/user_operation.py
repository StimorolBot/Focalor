from datetime import datetime
from fastapi_users import schemas

from pydantic import EmailStr
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_maker
from src.app.authentication.models.user import User
from src.app.authentication.models.news_letter import NewsLetter


class UserOperations:
    @staticmethod
    async def reset_password(password: str, user_email: EmailStr, session: AsyncSession):
        stmt = update(User).where(User.email == user_email).values({"password": password})
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def check_user_exists(log_data: str | EmailStr, session: AsyncSession):
        match log_data:
            case log_data if type(log_data) is EmailStr:
                query = select(User).where(User.email == log_data)
                execute_query = await session.execute(query)

            case log_data if type(log_data) is str:
                query = select(User).where(User.username == log_data)
                execute_query = await session.execute(query)

        print(execute_query)

    @staticmethod
    async def subscription_news_letter(user_email: EmailStr, session: AsyncSession):
        stmt = update(NewsLetter).where(NewsLetter.email == user_email).values({
            "is_subscription": True,
            "subscription_date": datetime.utcnow()})
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def add_role_and_newsletter(email: EmailStr, tables: list):
        async with async_session_maker() as session:
            user_id = select(User.id).where(User.email == email)
            for table in tables:
                stmt = insert(table).values({"user_id": user_id, "email": email})
                await session.execute(stmt)
                await session.commit()


user = UserOperations()
