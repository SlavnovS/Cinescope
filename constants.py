from enum import Enum


class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "login/"
REGISTER_ENDPOINT = "register/"
USER_ENDPOINT = "user/"

MOVIES_BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"
MOVIES_ENDPOINT = "movies/"

PAYMENT_BASE_URL = "https://payment.dev-cinescope.coconutqa.ru/"
PAYMENT_CREATE = "create"
PAYMENT_GET = "user"

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'