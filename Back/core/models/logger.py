from pydantic import BaseModel
from core.enum.logger_states import LoggerStates, LoggerDetail


class LoggerResponse(BaseModel):
    state: LoggerStates
    detail: LoggerDetail
    user_data: str

    @property
    def msg(self):
        return f"{self.state.value} --> {self.detail.value} --> {self.user_data}"
