from enum import Enum


class BatchStatus(Enum):
    PENDING = "PENDING"          # 생성된 상태
    PROCESSING = "PROCESSING"    # 처리 중
    COMPLETED = "COMPLETED"      # 완료됨
    FAILED = "FAILED"            # 실패
