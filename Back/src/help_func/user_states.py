from enum import Enum


class UserStates(Enum):
    ON_AFTER_REGISTER = 0
    EMAIL_CONFIRM = 1
    RESET_PASSWORD = 2
    CREATE = 3
