from enum import Enum


class PerformerType(Enum):
    REVIEWER = "REVIEWER"
    TESTER = "TESTER"


class CodeType(Enum):
    JAVA = "JAVA"
    PYTHON = "PYTHON"


class GenerativeAiType(Enum):
    OPENAI = "OpenAi"
