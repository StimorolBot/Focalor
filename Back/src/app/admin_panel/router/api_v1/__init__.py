from fastapi import APIRouter
from .router_admin import router_admin

router = APIRouter(tags=["api_v1"])
router.include_router(router_admin)