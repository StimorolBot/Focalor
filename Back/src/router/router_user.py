from fastapi import APIRouter, Request

from src.config import templates
from src.help_finc.get_list_img import get_list_img
from src.app.background_tasks.create_user_after_confirm_email import CreateUser

user = CreateUser()
router_user = APIRouter(tags=["pages"])


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

    if user.verified_token():
        await user.create()
        return templates.TemplateResponse("authentication/verified.html", {"request": request, "msg": "Успешное подтверждение почты !"})
