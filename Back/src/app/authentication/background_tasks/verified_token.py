from fastapi import status
from fastapi.responses import RedirectResponse


class VerifiedTokenUser:
    def __int__(self, token_request: str = None, token_render: str = None):
        self.token_request = token_request
        self.token_render = token_render

    def verified(self):
        if self.token_request is None or self.token_render is None:
            return RedirectResponse("/error", status_code=status.HTTP_408_REQUEST_TIMEOUT)

        elif self.token_request == self.token_render:
            return True

        else:
            return False


verified = VerifiedTokenUser()
