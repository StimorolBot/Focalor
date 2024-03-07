from fastapi import APIRouter
from .page_router import router as router_page
from .router import get_comment_user

rooter_comment = APIRouter(tags=["api_v1"])

rooter_comment.include_router(router_page)
rooter_comment.include_router(get_comment_user())
