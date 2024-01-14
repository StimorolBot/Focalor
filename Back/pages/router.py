from fastapi import APIRouter, Request
from src.config import templates

router_page = APIRouter(tags=["pages"])
router_authentication = APIRouter(tags=["authentication"])
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


@router_error.get("/error")
async def get_error_page(request: Request):
    return templates.TemplateResponse("error_page.html", {"request": request})
