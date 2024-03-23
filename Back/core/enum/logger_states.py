from enum import Enum


class LoggerStates(Enum):
    REQUEST = "Запрос"
    OK = "OK"
    ERROR = "Ошибка"


class LoggerDetail(Enum):
    MAIL_CONFIRMATION = "подтверждение почты"
    MAIL_CONFIRM = "почта подтверждена"
    LOGIN = "вход в систему"
    LOGOUT = "выход из системы"
    RESET_PASSWORD = "сброс пароля"
    SERVER_ERROR = "ошибка сервера"
    SUBSCRIBE_ON_NEWSLETTER = "подписка на рассылку"
