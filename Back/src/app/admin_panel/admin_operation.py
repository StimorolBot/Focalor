import uuid

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, status
from fastapi_users import FastAPIUsers
from fastapi.responses import RedirectResponse

from src.config import templates
from src.database import get_async_session
from src.app.authentication.models import User
from src.app.authentication.cookie import auth_backend
from src.app.authentication.user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend], )
current_user = fastapi_users.current_user()


async def check_admin(template: templates.TemplateResponse, user: User):
    try:
        if user.user_role == 0 and user.username == "admin":
            return template
    except AttributeError:
        return RedirectResponse("/error", status_code=status.HTTP_401_UNAUTHORIZED)


async def remove_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()
