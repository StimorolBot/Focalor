import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, status, HTTPException

from src.database import get_async_session
from src.app.authentication.models.user import User

from src.app.authentication.schemas.admmin import PaginationResponse
from fastapi_pagination import Page, paginate


class AdminOperations:
    @staticmethod
    async def check_admin(user: User):
        try:
            if user.is_superuser:
                return True
        except AttributeError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={"status_code": status.HTTP_404_NOT_FOUND,
                                        "data": "страница не найдена", }, )

    @staticmethod
    async def pagination(session: AsyncSession) -> Page[PaginationResponse]:
        query = select(User)
        query_execute = await session.execute(query)
        users = query_execute.all()
        user_list = [i[0].__dict__ for i in users]
        paginate_list, total, page, size, pages = paginate(user_list)
        pages = [i for i in range(1, pages[1] + 1)]

        return [paginate_list, total, page, size, pages]

    @staticmethod
    async def remove_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()
