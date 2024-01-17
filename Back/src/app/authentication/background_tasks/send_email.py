import smtplib

from email.message import EmailMessage
from src.config import celery, SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_TOKEN


def render_email_template(username: str) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Добро пожаловать !"
    email["From"] = SMTP_EMAIL
    email["To"] = SMTP_EMAIL

    email.set_content(
        "<div style = 'display:flex;flex-direction: column;'>"
        f"<h1 style = 'text-align:center'> Добро пожаловать, {username} ! </h1 >"
        "<img src = 'https://static.wikia.nocookie.net/genshin-impact/images/1/15/%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%9F%D0%B0%D0%B9%D0%BC%D0%BE%D0%BD"
        "_01_03.png/revision/latest/scale-to-width-down/250?cb=20211031090041&path-prefix=ru' style='width:200px; height: 200px;margin: 0 auto;'>"
        "</div>",
        subtype="html"
    )

    return email


@celery.task
def send_email_after_register(username: str):
    email = render_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(user=SMTP_EMAIL, password=SMTP_TOKEN)
        server.send_message(email)


"""
import string
import secrets
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.database import get_async_session

from src.app.authentication.models import User
# router = APIRouter(tags=['user', ])

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



"""
