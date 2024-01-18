import string
import smtplib
import secrets

from fastapi import Request

from email.message import EmailMessage
from src.app.authentication.background_tasks.verified_token import verified
from src.config import celery, SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_TOKEN


def render_email_on_after_register(username: str, email: EmailMessage) -> EmailMessage:
    email["Subject"] = "Добро пожаловать !"
    email.set_content(
        "<div style = 'display:flex; flex-direction: column;'>"
        f"<h1> Добро пожаловать, {username} ! </h1 >"
        "<img src = 'https://static.wikia.nocookie.net/genshin-impact/images/1/15/%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%9F%D0%B0%D0%B9%D0%BC%D0%BE%D0%BD"
        "_01_03.png/revision/latest/scale-to-width-down/250?cb=20211031090041&path-prefix=ru' style='width:200px; height: 200px;'>"
        "</div>",
        subtype="html"
    )

    return email


def render_email_token(request: Request) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(letters_and_digits) for _ in range(64))
    return f"{request.url.hostname}:{request.url.port}/is_verified/{token}"


def render_email_confirm(token_confirm, email: EmailMessage) -> EmailMessage:
    email["Subject"] = "Пожалуйста, подтвердите почту !"
    email.set_content(
        "<div'>"
        "<h2'>Для подтверждения почты, пожалуйста, перейдите по следующей ссылке:</h2 >"
        f"{token_confirm}"
        "</div>",
        subtype="html"
    )
    return email


@celery.task
def send_email(action: str, *args, **kwargs):
    email = EmailMessage()
    email["From"] = SMTP_EMAIL
    email["To"] = SMTP_EMAIL

    match action:
        case "on_after_register":
            render_email_on_after_register(email=email, username=kwargs["username"])
        case "email_confirm":
            render_token = render_email_token(kwargs["request"])
            verified.token_render = render_token.split("/")[2]
            render_email_confirm(email=email, token_confirm=render_token)
        case _:
            raise "[!] Неизвестное действие! Доступны: on_after_register,  email_confirm "

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(user=SMTP_EMAIL, password=SMTP_TOKEN)
        server.send_message(email)
