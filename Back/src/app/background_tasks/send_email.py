import smtplib

from email.message import EmailMessage
from src.help_func.user_states import UserStates
from src.config import celery, SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_TOKEN
from src.app.background_tasks.email_templates import (render_email_on_after_register,
                                                      render_email_confirm,
                                                      render_email_reset_password)


@celery.task
def send_email(state: UserStates, **kwargs):
    email = EmailMessage()
    email["From"] = SMTP_EMAIL
    email["To"] = SMTP_EMAIL

    match state.value:
        case "on_after_register":
            render_email_on_after_register(email=email, username=kwargs["username"])
        case "email_confirm":
            render_email_confirm(email=email, token=kwargs["token"])
        case "reset_password":
            render_email_reset_password(email=email)
        case _:
            raise "[!] неизвестное состояние"

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(user=SMTP_EMAIL, password=SMTP_TOKEN)
        server.send_message(email)
