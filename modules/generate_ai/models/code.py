from dataclasses import dataclass

from modules.generate_ai.models.open_ai_enums import CodeType, GenerativeAiType


@dataclass
class Code:
    code_type: CodeType
    ai_type: GenerativeAiType
    source: str