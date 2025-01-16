from enum import Enum


class CrawlerType(Enum):
    BEAUTIFUL_SOUP = "BEAUTIFUL_SOUP"
    SELENIUM = "SELENIUM"
    API = "API"



class AuthType(Enum):
    TOKEN = "TOKEN"
    LOGIN = "LOGIN"
    COOKIE = "COOKIE"
    NONE = "NONE"
