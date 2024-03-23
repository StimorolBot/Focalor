from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.openapi import OpenAPIResponseType
from fastapi import APIRouter, Depends, status
from fastapi_users.router.common import ErrorCode, ErrorModel

from src.app.authentication.models.user import User
from src.app.authentication.schemas.user_auth import UserResetPassword
from src.app.authentication.user_manager import UserManager, get_user_manager
from src.app.authentication.operations.user_operation import user as user_operation

from core.operation.crud import Crud
from core.database import get_async_session
from core.operation.convert import get_to_redis
from core.schemas.response import Response as ResponseSchemas


def get_reset_password_user() -> APIRouter:
    router = APIRouter()
    reset_password_response: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.RESET_PASSWORD_BAD_TOKEN: {
                            "summary": "Bad or expired token.",
                            "value": {"detail": ErrorCode.RESET_PASSWORD_BAD_TOKEN},
                        },
                        ErrorCode.RESET_PASSWORD_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                                    "reason": "Password should be at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    }

    @router.patch("/reset-password", name="reset:reset_password", responses=reset_password_response, )
    async def reset_password(session: AsyncSession = Depends(get_async_session),
                             user_data: UserResetPassword = Depends(UserResetPassword),
                             user_manager: UserManager = Depends(get_user_manager)):
        user = await user_operation.check_user_exists(log_data=user_data.email, session=session)

        if user is not None:
            token = await get_to_redis(key=user[0].email)

            if token["token"] == user_data.token:
                hashed_password = user_manager.password_helper.hash(user_data.password)

                data = {"hashed_password": hashed_password}
                await Crud.update(session=session, table=User, update_field=User.hashed_password, update_where=user_data.email, data=data)
                await user_manager.on_after_reset_password(user_data)
                return ResponseSchemas(status_code=status.HTTP_200_OK, data="Пароль успешно сброшен")

    return router
