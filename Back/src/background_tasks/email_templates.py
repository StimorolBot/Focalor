from email.message import EmailMessage


def render_email_on_after_register(username: str, email: EmailMessage, email_subject: str) -> EmailMessage:
    email["Subject"] = email_subject
    email.set_content(
        "<div style = 'display: flex; flex-direction: column; align-items: center;'>"
        f"<h1> Добро пожаловать, {username} ! </h1 >"
        "<img src = 'https://static.wikia.nocookie.net/genshin-impact/images/1/15/%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%9F%D0%B0%D0%B9%D0%BC%D0%BE%D0%BD"
        "_01_03.png/revision/latest/scale-to-width-down/250?cb=20211031090041&path-prefix=ru' style='width:200px; height: 200px;'>"
        "</div>",
        subtype="html"
    )

    return email


def render_email_confirm(token, email: EmailMessage, email_subject: str) -> EmailMessage:
    email["Subject"] = email_subject
    email.set_content(
        "<div'>"
        "<h2'>Для подтверждения почты, пожалуйста, перейдите по следующей ссылке:</h2 >"
        f"{token}"
        "</div>",
        subtype="html"
    )
    return email


def render_email_reset_password(email: EmailMessage, email_subject: str, token: str) -> EmailMessage:
    email["Subject"] = email_subject

    email.set_content(
        "<div>"
        f"<h1>Для сброса пароля введите: {token}</h1 >"
        "<h2>Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо</h2>"
        "</div>",
        subtype="html"
    )
    return email
