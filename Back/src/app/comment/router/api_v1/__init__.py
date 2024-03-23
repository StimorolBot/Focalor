from fastapi import APIRouter
from .router import router_comment

rooter_comment = APIRouter(tags=["api_v1"])

rooter_comment.include_router(router_comment)
