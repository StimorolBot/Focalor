from fastapi_users import exceptions
from fastapi import APIRouter, Request, Depends

from src.config import templates
from src.help_func.get_list_img import get_list_img
from src.app.authentication.operations.user_operation import user
from src.app.authentication.user_manager import get_user_manager, UserManager

router_user = APIRouter(tags=["user"])


@router_user.get("/")
async def get_home_page(request: Request):
    list_img_slider = await get_list_img(path="../Front/img/slider")
    list_img_bg = await get_list_img(path="../Front/img/bg")
    return templates.TemplateResponse("main.html", {"request": request, "title": "Focalors",
                                                    "list_img_slider": list_img_slider, "list_img_bg": list_img_bg,
                                                    "indicators": len(list_img_bg)})


@router_user.get("/verified/{token}")
async def get_verified_page(request: Request):
    user.token_request = request["path"].split("/")[2]
    if await user.verified_token() is True:
        await user.create()
        return templates.TemplateResponse("authentication/verified.html", {"request": request, "title": "Verified",
                                                                           "msg": "Успешное подтверждение почты !"})


@router_user.post("/subscribe")
async def subscribe_newsletter(request: Request, user_manager: UserManager = Depends(get_user_manager)):
    data = await request.json()
    try:
        await user_manager.get_by_email(data["email"].replace("%", "@"))
    except exceptions.UserNotExists:
        print(f"[!] Почта {data['email'].replace('%', '@')} не найдена")
    return await request.json()
