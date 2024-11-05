from enum import Enum


class AuthType(Enum):
    TOKEN = "TOKEN"
    LOGIN = "LOGIN"
    COOKIE = "COOKIE"
    NONE = "NONE"
