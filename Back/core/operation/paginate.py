from typing import TYPE_CHECKING, Optional

from fastapi_pagination.utils import verify_params
from fastapi_pagination.bases import AbstractParams

from sqlalchemy import select, desc
from src.app.comment.models import Comment

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

async def paginate(page: int, session: "AsyncSession", params: Optional[AbstractParams] = None) -> list:
    params, raw_params = verify_params(params, "limit-offset")
    offset = raw_params.limit * (page - 1)

    query = select(Comment).order_by(desc(Comment.data_comment)).limit(raw_params.limit).offset(offset)
    query = await session.execute(query)

    return  [item_dict.__dict__ for item in query.all() for item_dict in item][::-1]
