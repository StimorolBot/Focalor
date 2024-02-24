from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_users.router.common import ErrorCode, ErrorModel

from fastapi import APIRouter, Depends, Request, status
from fastapi_users.openapi import OpenAPIResponseType

from src.database import get_async_session
from src.app.comment.operations import CommentOperations
from src.app.comment.schemas import Comment as CommentSchemas
from src.app.authentication.user_manager import current_user


def get_comment_router() -> APIRouter:
    router = APIRouter()

    comment_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                              "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    }

    @router.post("/comment", responses=comment_responses)
    async def create_comment(request: Request, user=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
        data = await request.json()
        comment = data["comment"]

        comment_dict = CommentSchemas(user_id=user.id, comment=comment).model_dump()
        await CommentOperations.create_comment(session=session, comment_dict=comment_dict)

    return router
