from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, status
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel


from core.schemas.response import Response
from core.database import get_async_session
from src.router.router_user import seng_code_reset_psd
from src.app.authentication.schemas.user_auth import UserResetPassword
from src.app.authentication.operations.user_operation import user as user_operation


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

    # patch меняет указанное поле, остальное не трогает
    # put меняет указанное поле, остальные поля сбрасывает
    @router.patch("/reset-password", name="reset:reset_password", responses=reset_password_response, )
    async def reset_password(request: Request, user: UserResetPassword = Depends(UserResetPassword),
                             session: AsyncSession = Depends(get_async_session),
                             ) -> Response:

        data = await request.json()
        data_email = data["email"].replace("%40", "@")
        token_response = data["token"]


        #await user_operation.check_user_exists(log_data=data_email, session=session)

        #token_generate = get_token(states=UserStates.RESET_PASSWORD, request=request)
        #send_email(state=UserStates.RESET_PASSWORD, token=token_generate["token"], user_email=data_email)

       # if token_response == token_generate and await user_operation.ttl_check(ttl=token_generate["ttl"]):
            #await user_operation.reset_password(password=user.password, user_email=user.email, session=session)

        #return Response(status_code=status.HTTP_200_OK, data="Пароль успешно сброшен")

    return router


# отдельный роутер для отправки на эмейла
#