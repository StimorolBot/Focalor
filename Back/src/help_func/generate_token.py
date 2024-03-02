import string
import secrets
from typing import Optional
from fastapi import Request
from core.enum.email_states import EmailStates


def render_token(token_len: int = 64) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(letters_and_digits) for _ in range(token_len))
    return token


def get_token(states: EmailStates, request: Optional[Request] = None) -> list | str:
    match states.value:
        case "email_confirm":
            token = render_token()
            url = f"{request.url.hostname}:{request.url.port}/verified/{token}"
            return [token, url]
        case "reset_password":
            return render_token(token_len=6)
        case _:
            raise "[!] неизвестное состояние"
