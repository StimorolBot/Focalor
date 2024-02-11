import string
import secrets
from typing import Optional
from fastapi import Request
from datetime import datetime, timedelta

from src.config import LIFETIME
from src.app.authentication.operations.states import UserStates


def render_token(token_len: int, lifetime_seconds: int) -> dict:
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(letters_and_digits) for _ in range(token_len))
    ttl = datetime.utcnow() + timedelta(seconds=int(lifetime_seconds))
    return {"token": token, "ttl": ttl}


def get_token(states: UserStates, request: Optional[Request] = None) -> dict:
    match states.value:
        case "email_confirm":
            data = render_token(token_len=64, lifetime_seconds=LIFETIME)
            data["token"] = f"{request.url.hostname}:{request.url.port}/verified/{data['token']}"
            return data
        case "reset_password":
            return render_token(token_len=6, lifetime_seconds=LIFETIME)
        case _:
            raise "[!] неизвестное состояние"
