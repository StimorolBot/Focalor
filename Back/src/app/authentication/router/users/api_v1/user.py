from typing import TYPE_CHECKING
from fastapi import APIRouter, Request, Depends, HTTPException, status

from core.config import templates
from core.database import get_async_session
from core.enum.email_states import EmailStates

from sqlalchemy.ext.asyncio import AsyncSession

from src.help_func.generate_token import get_token
from src.help_func.get_list_img import get_list_img
from src.background_tasks.send_email import send_email
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


@router_user.post("/reset-password/code-confirm")
async def seng_code_reset_psd(request: Request):  # CheckEmail
    data = await request.json()
    data_email = data["email"].replace("%40", "@")

    token_generate = get_token(states=EmailStates.RESET_PASSWORD, request=request)
    send_email(state=EmailStates.RESET_PASSWORD, token=token_generate["token"], user_email=data_email)
