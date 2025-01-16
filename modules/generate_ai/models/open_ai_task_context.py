from dataclasses import dataclass

from modules.generate_ai.models.open_ai_enums import PerformerType
from modules.generate_ai.models.task_context import TaskContext


@dataclass
class OpenAiTaskContext(TaskContext):
    system_message: str  # 시스템 메시지
    user_message: str  # 유저 메시지
    perform_type: PerformerType
    model: str = "gpt-4o"  # 사용할 모델 (기본값: gpt-4)
    temperature: float = 0.7  # 샘플링 온도 (기본값: 0.7)
    is_realtime: bool = True  # 실시간 실행 여부 (기본값: True)

