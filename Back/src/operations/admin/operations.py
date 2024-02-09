import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, status, HTTPException

from src.config import templates
from src.database import get_async_session
from src.app.authentication.models import User


class AdminOperations:
    @staticmethod
    async def check_admin(template: templates.TemplateResponse, user: User):
        try:
            if user.is_superuser:
                return template
        except AttributeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail={"status": status.HTTP_401_UNAUTHORIZED, "data": "Пользователь не авторизован", }, )

    @staticmethod
    async def remove_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()
