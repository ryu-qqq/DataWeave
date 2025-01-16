from enum import Enum


class Action(Enum):
    SAVE_S3 = "SAVE_S3"
    SAVE_CACHE = "SAVE_CACHE"
    API_CALL = "API_CALL"


class Target(Enum):
    RAW_DATA = "RAW_DATA"
    CACHE = "CACHE"
    PRODUCT = "PRODUCT"
