import smtplib

from email.message import EmailMessage
from src.app.authentication.operations.states import UserStates
from src.config import celery, SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_TOKEN
from src.background_tasks.email_templates import (render_email_on_after_register, render_email_confirm,
                                                  render_on_after_reset_password, render_email_reset_password)


@celery.task
def send_email(state: UserStates, **kwargs):
    email = EmailMessage()
    email["From"] = SMTP_EMAIL
    email["To"] = SMTP_EMAIL

    match state.value:
        case "on_after_register":
            render_email_on_after_register(email=email, username=kwargs["username"], email_subject="Добро пожаловать !")
        case "email_confirm":
            render_email_confirm(email=email, token=kwargs["token"], email_subject="Подтверждение почты")
        case "reset_password":
            render_email_reset_password(email=email, email_subject="Сброс пароля", token=kwargs["token"])
        case "on_after_reset_password":
            render_on_after_reset_password(email=email, email_subject="Сброс пароля")
        case _:
            raise "[!] неизвестное состояние"

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(user=SMTP_EMAIL, password=SMTP_TOKEN)
        server.send_message(email)
