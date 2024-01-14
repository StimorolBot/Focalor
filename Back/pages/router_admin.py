from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.responses import RedirectResponse

from fastapi_pagination.links import Page
from fastapi_pagination import paginate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import templates
from src.database import get_async_session
from src.app.authentication.models import User
from src.app.admin_panel.schemas import ServerResponse
from src.app.admin_panel.admin_operation import select_user, check_current_user

router_admin = APIRouter(tags=["admin"])


@router_admin.get("/admin_panel")
async def get_admin_panel(request: Request, users_info=Depends(select_user), user=Depends(check_current_user)):
    match user:
        case "admin":
            if len(users_info) != 0:
                return templates.TemplateResponse("admin/admin.html", {"request": request, "users": users_info})
            else:
                return RedirectResponse("/error")
        case _:
            return RedirectResponse("/error")


@router_admin.get("/users__")
async def pagination(session: AsyncSession = Depends(get_async_session)) -> Page[ServerResponse]:
    query = select(User)
    query_execute = await session.execute(query)
    users = query_execute.all()
    user_list = [i[0].__dict__ for i in users]
    return paginate(user_list)
