from fastapi import APIRouter

from .user import router_user
from .admin import router_admin

router = APIRouter(tags=["api_v1"])

router.include_router(router_admin)
router.include_router(router_user)
