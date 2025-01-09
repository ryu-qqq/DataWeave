from enum import Enum


class BatchStatus(Enum):
    PENDING = "PENDING"  # 배치 생성 대기 중
    PROCESSING = "PROCESSING"  # 배치 처리 중
    COMPLETED = "COMPLETED"  # 최종 완료
    ENHANCED = "ENHANCED"  # 일부 데이터 누락
    READY_FOR_REVIEW = "READY_FOR_REVIEW"  # 검토 준비 완료
    FAILED = "FAILED"  # 실패, 재시도 가능
    EXHAUSTED = "EXHAUSTED"  # 재시도 횟수 초과, 처리 불가능
