from fastapi import APIRouter
from .router import router_home

router = APIRouter(tags=["api_v1"])
router.include_router(router_home)
