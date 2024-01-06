from fastapi import Depends
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from src.config import templates

from src.app.admin_panel.admin_operation import select_user, check_current_user

router_page = APIRouter(tags=["pages"])
router_authentication = APIRouter(tags=["authentication"])
router_admin = APIRouter(tags=["admin"])
router_error = APIRouter(tags=["error"])


@router_page.get("/")
async def get_home_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router_authentication.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("authentication/login.html", {"request": request})


@router_authentication.get("/register")
async def get_register_page(request: Request):
    return templates.TemplateResponse("authentication/register.html", {"request": request})


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


@router_error.get("/error")
async def get_error_page(request: Request):
    return templates.TemplateResponse("error_page.html", {"request": request})
