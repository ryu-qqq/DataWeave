from enum import Enum


class MergeStatus(str, Enum):
    OPENED = "OPENED"
    SYNCHRONIZE = "SYNCHRONIZE"
    CLOSED = "CLOSED"

    @staticmethod
    def of(name: str) -> "MergeStatus":
        return MergeStatus[name.upper()] if name.upper() in MergeStatus.__members__ else MergeStatus.OPENED

    def is_opened(self) -> bool:
        return self == MergeStatus.OPENED


class ReviewStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class GitType(str, Enum):
    GIT_HUB = "GIT_HUB"
    GIT_LAB = "GIT_LAB"


class ChangeType(str, Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"
