from typing import TYPE_CHECKING
from fastapi import APIRouter, Request, Depends

from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import templates
from src.help_func.get_list_img import get_list_img
from src.app.authentication.user_manager import current_user
from src.app.authentication.operations.user_operation import user

if TYPE_CHECKING:
    from src.app.authentication.models.user import User as UserTable

router_user = APIRouter(tags=["user"])


@router_user.get("/")
async def get_home_page(request: Request):
    list_img_slider = await get_list_img(path="../Front/img/slider")
    list_img_bg = await get_list_img(path="../Front/img/bg")
    return templates.TemplateResponse("page/main.html", {"request": request, "title": "Focalors",
                                                         "list_img_slider": list_img_slider, "list_img_bg": list_img_bg,
                                                         "indicators": len(list_img_bg)})


@router_user.get("/verified/{token}")
async def get_verified_page(request: Request, token: str):
    if await user.verified_token(token_request=token) is True:
        await user.create_user()
        return templates.TemplateResponse("verified.html", {"request": request, "title": "Verified",
                                                            "msg": "Успешное подтверждение почты !"})


@router_user.post("/subscribe")
async def subscribe_newsletter(request: Request, cur_usr: "UserTable" = Depends(current_user),
                               session: AsyncSession = Depends(get_async_session)):
    data = await request.json()
    data_email = data["email"].replace("%40", "@")

    if cur_usr.email == data_email:
        await user.subscription_news_letter(cur_usr.email, session)

    return await request.json()


@router_user.get("/comment")
async def get_comment_page(request: Request):
    return templates.TemplateResponse("page/comment.html", {"request": request, "title": "Comment"})
