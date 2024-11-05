from enum import Enum


class ActionType(Enum):
    SAVE_CACHE = "SAVE_CACHE"
    SAVE_S3 = "SAVE_S3"
    CALL_SERVER = "CALL_SERVER"
    EXTRACT = "EXTRACT"
    NONE = "NONE"
