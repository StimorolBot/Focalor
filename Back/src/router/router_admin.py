from fastapi import Depends
from fastapi import APIRouter, Request, Query

from fastapi_pagination import Page, paginate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import templates
from core.database import get_async_session
from src.app.authentication.models.user import User
from src.app.authentication.user_manager import current_user
from src.app.authentication.schemas.admmin import PaginationResponse
from src.app.authentication.operations.admin_operations import AdminOperations

router_admin = APIRouter(tags=["admin"])
admin_operation = AdminOperations()
Page = Page.with_custom_options(size=Query(default=5, ge=3, le=6))


@router_admin.get("/admin")
async def get_admin(request: Request, user=Depends(current_user)):
    return await admin_operation.check_admin(template=templates.TemplateResponse("admin/admin.html",
                                                                                 {"request": request, "title": "Admin"}), user=user)


@router_admin.get("/admin/table")
async def pagination(request: Request, session: AsyncSession = Depends(get_async_session),
                     user=Depends(current_user)) -> Page[PaginationResponse]:
    query = select(User)
    query_execute = await session.execute(query)
    users = query_execute.all()
    user_list = [i[0].__dict__ for i in users]
    paginate_list, total, page, size, pages = paginate(user_list)
    pages = [i for i in range(1, pages[1] + 1)]
    return await admin_operation.check_admin(template=templates.TemplateResponse("admin/admin_table.html",
                                                                                 {"request": request, "users": paginate_list[1],
                                                                                  "btns": pages, "title": "Users table"}), user=user)
