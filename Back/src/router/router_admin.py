from fastapi import Depends
from fastapi import APIRouter, Request, Query

from fastapi_pagination import Page, paginate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import templates
from src.database import get_async_session
from src.app.authentication.models import User
from src.app.admin_panel.schemas import ServerResponse
from src.app.admin_panel.admin_operation import check_admin
from src.app.admin_panel.admin_operation import current_user

router_admin = APIRouter(tags=["admin"])
Page = Page.with_custom_options(size=Query(default=5, ge=3, le=6))


@router_admin.get("/admin")
async def get_admin(request: Request, user=Depends(current_user)):
    return await check_admin(template=templates.TemplateResponse("admin/admin.html", {"request": request}), user=user)


@router_admin.get("/admin/table")
async def pagination(request: Request, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)) -> Page[ServerResponse]:
    query = select(User)
    query_execute = await session.execute(query)
    users = query_execute.all()
    user_list = [i[0].__dict__ for i in users]
    paginate_list, total, page, size, pages = paginate(user_list)
    pages = [i for i in range(1, pages[1] + 1)]
    return await check_admin(template=templates.TemplateResponse("admin/admin_table.html",
                                                                 {"request": request, "users": paginate_list[1],
                                                                  "btns": pages}), user=user)
