import string
import secrets
#import smtplib

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.database import get_async_session

from src.app.authentication.models import User
from src.app.admin_panel.admin_operation import current_user

from src.config import SMTP_PORT, SMTP_HOST, EMAIL, PASSWORD

router = APIRouter(tags=['user', ])


@router.patch("/reset_password")
async def reset_user_password():
    return "Work!"


async def generate_code_confirm() -> str:
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(secrets.choice(letters_and_digits) for _ in range(8))


async def get_user_email(user=Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> str | AttributeError:
    try:
        query = select(User).where(User.email == user.email)
        execute_query = await session.execute(query)
        return execute_query.mappings().all()[0]["User"]
    except AttributeError as e:
        return e


async def generate_template_email_code_confirm(user_info=Depends(get_user_email)):
    code = await generate_code_confirm()
    return code


"""@router.get("/test")
async def send_msg():
    email_content = await generate_template_email_code_confirm()

    with smtplib.SMTP_SSL(SMTP_PORT, SMTP_HOST) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(email_content)
        return "200"
"""
