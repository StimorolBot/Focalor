from typing import TYPE_CHECKING

from sqlalchemy import select, insert

from src.app.authentication.models.user import User

if TYPE_CHECKING:
    from pydantic import EmailStr
    from sqlalchemy.ext.asyncio import AsyncSession


class UserOperations:

    @staticmethod
    async def check_user_exists(log_data: str, session: "AsyncSession"):
        match len(log_data.split("@")):
            case 2:
                query = select(User).where(User.email == log_data)
                execute_query = await session.execute(query)
            case 1:
                query = select(User).where(User.username == log_data)
                execute_query = await session.execute(query)
            case _:
                raise AttributeError("[!] Не удалось получить логин")

        return execute_query.one_or_none()

    @staticmethod
    async def add_role_and_newsletter(email: "EmailStr", tables: list, session: "AsyncSession"):
        user = select(User.id).where(User.email == email).scalar_subquery()
        for table in tables:
            stmt = insert(table).values({"user_id": user, "email": email})
            await session.execute(stmt)
            await session.commit()


user = UserOperations()
