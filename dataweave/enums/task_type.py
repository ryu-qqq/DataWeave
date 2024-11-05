from enum import Enum


class TaskType(Enum):
    NAVIGATE = "NAVIGATE"
    EXTRACT = "EXTRACT"
    CLICK = "CLICK"
    INPUT = "INPUT"
    API_CALL = "API_CALL"
    X_COM = "X_COM"
    NONE = "NONE"
