import json

from core.config import redis
from core.schemas.response import Response as ResponseSchemas

from fastapi_users.openapi import OpenAPIResponseType
from fastapi import APIRouter, Depends, HTTPException, Request, status
from src.app.authentication.user_manager import UserManager, get_user_manager

from fastapi_users.router.common import ErrorCode, ErrorModel
from src.app.authentication.schemas.user_auth import UserCreate


def get_verify_user(user_create_schema: UserCreate) -> APIRouter:
    router = APIRouter()

    verify_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.VERIFY_USER_BAD_TOKEN: {
                            "summary": "Bad token, not existing user or"
                                       "not the e-mail currently set for the user.",
                            "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                        },
                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                            "summary": "The user is already verified.",
                            "value": {
                                "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                            },
                        },
                    }
                }
            },
        }
    }

    @router.get("/verified/{token}", name="verify:verify", responses=verify_responses)
    async def verify(request: Request, token: str, user_manager: UserManager = Depends(get_user_manager), ):
        user_str = await redis.get(token)

        if user_str is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="verify_responses")

        user_dict = json.loads(user_str)
        user_create = user_create_schema(**user_dict)
        await user_manager.create(user_create=user_create)

        return ResponseSchemas(status_code=status.HTTP_201_CREATED, data="verify_responses")

    return router
