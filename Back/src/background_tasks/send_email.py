import smtplib

from email.message import EmailMessage
from src.background_tasks import email_templates

from core.config import celery, setting
from core.enum.email_states import EmailStates


@celery.task
def send_email(state: EmailStates, **kwargs):
    email = EmailMessage()
    email["From"] = setting.SMTP_EMAIL
    email["To"] = setting.SMTP_EMAIL

    match state.value:
        case "on_after_register":
            email_templates.render_email_on_after_register(email=email, username=kwargs["username"], email_subject="Добро пожаловать !")
        case "email_confirm":
            email_templates.render_email_confirm(email=email, token=kwargs["token"], email_subject="Подтверждение почты")
        case "reset_password":
            email_templates.render_email_reset_password(email=email, email_subject="Сброс пароля", token=kwargs["token"])
        case "on_after_reset_password":
            email_templates.render_on_after_reset_password(email=email, email_subject="Сброс пароля")
        case _:
            raise "[!] неизвестное состояние"

    with smtplib.SMTP_SSL(setting.SMTP_HOST, setting.SMTP_PORT) as server:
        server.login(user=setting.SMTP_EMAIL, password=setting.SMTP_TOKEN)
        server.send_message(email)
