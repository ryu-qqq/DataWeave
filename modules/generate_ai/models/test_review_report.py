import json
from dataclasses import dataclass

from modules.generate_ai.models.report import Report


@dataclass
class TestCodeReport(Report):
    suggested_code: str

    def to_string(self) -> str:
        return (
            f"Suggested Code:\n{self.suggested_code}\n\n"
        )

    def to_json(self) -> str:
        return json.dumps({
            "suggested_code": self.suggested_code
        }, ensure_ascii=False)