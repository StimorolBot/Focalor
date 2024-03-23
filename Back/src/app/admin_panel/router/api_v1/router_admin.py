from fastapi import Depends
from fastapi import APIRouter, Request, Query

from fastapi_pagination import Page, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import templates
from core.database import get_async_session
from src.app.authentication.models.user import User
from src.app.authentication.user_manager import current_user
from src.app.admin_panel.schemas.admmin import PaginationResponse

from core.operation.crud import Crud

router_admin = APIRouter(tags=["admin"])
Page = Page.with_custom_options(size=Query(default=5, ge=3, le=6))


@router_admin.get("/admin")
async def get_admin(request: Request, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)) -> Page[PaginationResponse]:
    if user.is_superuser:
        user_list = await Crud.read_all(table=User, session=session)
        paginate_list, _, _, _, pages = paginate(user_list)
        return templates.TemplateResponse("page/admin/admin.html", {"request": request, "title": "Admin",
                                                                    "users": paginate_list[1], "btns": pages[1]})
