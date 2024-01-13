import uuid

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.database import get_async_session
from src.app.authentication.models import User

from src.app.authentication.user_manager import get_user_manager
from fastapi_users import FastAPIUsers
from src.app.authentication.cookie import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend], )
current_user = fastapi_users.current_user()

router = APIRouter(prefix="/admin_panel", tags=['admin', ])


async def select_user(offset: int = 1, session: AsyncSession = Depends(get_async_session)):
    match offset:
        case 1:
            query = select(User).limit(2)
        case 2:
            query = select(User).limit(2).offset(offset)
        case _:
            offset = offset + (offset - 2)
            query = select(User).limit(2).offset(offset)
    query_execute = await session.execute(query)
    return query_execute.mappings().all()


async def check_current_user(user=Depends(current_user)):
    try:
        if user.user_role == 0 and user.username == "admin":
            return "admin"
        else:
            return "user"
    except AttributeError:
        return "unauthorized"


async def remove_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()
