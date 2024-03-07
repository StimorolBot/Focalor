from enum import Enum


class EmailStates(Enum):
    ON_AFTER_REGISTER = "on_after_register"
    EMAIL_CONFIRM = "email_confirm"
    RESET_PASSWORD = "reset_password"
    CREATE_USER = "create_user"
    ON_AFTER_RESET_PASSWORD = "on_after_reset_password"
