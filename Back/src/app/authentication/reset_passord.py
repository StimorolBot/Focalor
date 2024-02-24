from fastapi import APIRouter, Depends, HTTPException, Request, status

from fastapi_users import exceptions, models
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

from src.app.authentication.schemas.user_auth import UserResetPassword
from src.background_tasks.send_email import send_email

RESET_PASSWORD_RESPONSES: OpenAPIResponseType = {
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


def get_reset_password_router(get_user_manager: UserManagerDependency[models.UP, models.ID], ) -> APIRouter:
    router = APIRouter()

    # patch меняет указанное поле, остальное не трогает
    # put меняет указанное поле, остальные поля сбрасывает
    @router.patch("/reset-password", name="reset:reset_password", responses=RESET_PASSWORD_RESPONSES, )
    async def reset_password(request: Request, user: UserResetPassword = Depends(UserResetPassword),
                             user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager), ):
        send_email("reset_password")

        try:
            await user_manager.reset_password(user.token, user.password, request)

        except (exceptions.InvalidResetPasswordToken, exceptions.UserNotExists, exceptions.UserInactive,):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN, )

        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )

    return router


"""
@router.patch("/reset-password", name="reset:reset_password", responses=RESET_PASSWORD_RESPONSES, )
    async def reset_password(request: Request, email: EmailStr = Body(...), token: str = Body(...), password: str = Body(...),
                             user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager), ):
        try:
            await user_manager.reset_password(token, password, request)

        except (exceptions.InvalidResetPasswordToken, exceptions.UserNotExists, exceptions.UserInactive,):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN, )

        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )

    return router



"""
