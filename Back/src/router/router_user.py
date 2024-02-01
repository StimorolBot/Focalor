from fastapi import APIRouter, Request, HTTPException, status

from src.config import templates
from src.app.background_tasks.create_user_after_confirm_email import CreateUser

user = CreateUser()
router_user = APIRouter(tags=["pages"])


@router_user.get("/")
async def get_home_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router_user.get("/verified/{token}")
async def get_verified_page(request: Request):
    user.token_request = request["path"].split("/")[2]

    if user.verified_token():
        await user.create()
        return templates.TemplateResponse("authentication/verified.html", {"request": request, "msg": "Успешное подтверждение почты !"})
