import json
from typing import TYPE_CHECKING
from urllib.parse import unquote
from fastapi_pagination import Page
from fastapi import APIRouter, Request, Depends, Query

from src.app.authentication.user_manager import current_user
from src.app.comment.schemas import Comment as CommentSchemas

from core.config import templates
from core.operation.crud import Crud
from src.app.comment.models import Comment
from core.database import get_async_session
from core.operation.paginate import paginate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.app.authentication.models.user import User

router_comment = APIRouter(tags=["comment"])
Page = Page.with_custom_options(size=Query(default=20, ge=15, le=25))


@router_comment.get("/comment", response_model=Page[CommentSchemas])
async def get_comment_page(request: Request, session: "AsyncSession" = Depends(get_async_session), user: "User" = Depends(current_user)):
    page = unquote(request.url.query)

    match page:
        case page if page == "":
            page = 1
        case page if len(page) != 0:
            page = json.loads(page)["page"]

    comment = await paginate(page=page, session=session)
    return templates.TemplateResponse("page/comment.html", {"request": request, "title": "Comment", "uuid": user.id,
                                                            "username": user.username, "comment_list": comment})


@router_comment.post("/comment")
async def create_comment(request: Request, session: "AsyncSession" = Depends(get_async_session), user: "User" = Depends(current_user)):
    # передать user id через ajax или получить из сесии
    data = await request.json()
    comment = unquote(data["comment"])

    user_dict = CommentSchemas(user_id=user.id, comment=comment).model_dump()
    await Crud.create(session=session, data_dict=user_dict, table=Comment)

    return comment
