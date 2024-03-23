from fastapi import APIRouter

from src.app.authentication.user_manager import get_user_manager
from src.app.authentication.cookie import auth_backend
from src.app.authentication.schemas.user_auth import UserCreate
from src.app.authentication.models.user import User
from src.app.authentication.fastapi_users_custom import FastAPIUsers

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend], )

router_auth = APIRouter(tags=["api_v1"])

router_auth.include_router(fastapi_users.get_login_router(auth_backend), tags=["auth"], )
router_auth.include_router(fastapi_users.get_logout_router(auth_backend), tags=["auth"], )
router_auth.include_router(fastapi_users.get_register_router(UserCreate), tags=["auth"], )
router_auth.include_router(fastapi_users.get_reset_password_router(), tags=["auth"], )
router_auth.include_router(fastapi_users.get_verify_router(), tags=["auth"], )
