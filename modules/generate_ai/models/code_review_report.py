import json
from dataclasses import dataclass

from modules.generate_ai.models.report import Report


@dataclass
class CodeReviewReport(Report):
    review: str
    suggested_code: str
    test_required: bool

    def to_string(self) -> str:
        return (
            f"Review:\n{self.review}\n\n"
            f"Suggested Code:\n{self.suggested_code}\n\n"
            f"Test Required: {'Yes' if self.test_required else 'No'}"
        )

    def to_json(self) -> str:
        return json.dumps({
            "review": self.review,
            "suggested_code": self.suggested_code,
            "test_required": self.test_required
        }, ensure_ascii=False)