from src.config import JWT_TOKEN
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy

cookie_transport = CookieTransport(cookie_name="user_auth", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_TOKEN, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy, )
