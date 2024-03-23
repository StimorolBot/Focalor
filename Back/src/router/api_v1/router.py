from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import unquote
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Depends, status

from src.background_tasks.send_email import send_email
from src.app.authentication.user_manager import current_user
from src.app.authentication.models.news_letter import NewsLetter
from src.app.authentication.user_manager import get_user_manager

from core.config import templates
from core.operation.crud import Crud
from core.logger.logger import logger
from core.database import get_async_session
from core.enum.email_states import EmailStates
from core.operation.convert import add_to_redis
from core.operation.generate_token import get_token
from core.operation.get_list_img import get_list_img
from core.schemas.response import Response as ResponseSchemas

if TYPE_CHECKING:
    from src.app.authentication.user_manager import UserManager
    from src.app.authentication.models.user import User as UserTable

router_home = APIRouter(tags=["user"])


@router_home.get("/")
async def get_home_page(request: Request):
    list_img_slider = await get_list_img(path="../Front/img/slider")
    list_img_bg = await get_list_img(path="../Front/img/bg")
    return templates.TemplateResponse("page/main.html", {"request": request, "title": "Focalors",
                                                         "list_img_slider": list_img_slider, "list_img_bg": list_img_bg,
                                                         "indicators": len(list_img_bg)})


@router_home.post("/subscribe")
async def subscribe_newsletter(request: Request, cur_usr: "UserTable" = Depends(current_user),
                               session: AsyncSession = Depends(get_async_session),
                               user_manager:"UserManager"= Depends(get_user_manager)) -> ResponseSchemas:
    data = await request.json()
    data_email = unquote(data["email"])

    if cur_usr.email == data_email:
        data = {"is_subscription": True, "subscription_date": datetime.utcnow()}
        await Crud.update(session=session, table=NewsLetter, update_field=NewsLetter.email, update_where=cur_usr.email, data=data)
        await user_manager.on_after_subscribe(email=data_email)

    return ResponseSchemas(status_code=status.HTTP_200_OK, data="Вы подписались на рассылку")


@router_home.post("/reset-password/code-confirm")
async def seng_code_reset_psd(request: Request):  # CheckEmail
    data = await request.json()

    if data.get("email"):
        data_email = unquote(data["email"])
        token = get_token(states=EmailStates.RESET_PASSWORD, request=request)

        user_dict = {"token": token}
        await add_to_redis(user_data=user_dict, name=data_email)

        send_email(state=EmailStates.RESET_PASSWORD, token=token, user_email=data_email)
        logger.info(f"Запрос на сброс пароля: {data_email}")
        return ResponseSchemas(status_code=status.HTTP_200_OK, data="Письмо отправлено на почту")

    else:
        return ResponseSchemas(status_code=status.HTTP_400_BAD_REQUEST, data="Не удалось получить содержимое поля: 'email' ")
