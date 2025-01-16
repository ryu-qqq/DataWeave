import json

from injector import singleton, Injector

from modules.generate_ai.executor.report_generator import ReportGenerator
from modules.generate_ai.models.open_ai_enums import PerformerType
from modules.generate_ai.models.code_review_report import CodeReviewReport


@singleton
class ReviewReportGenerator(ReportGenerator):

    def supports(self, performer_type: PerformerType) -> bool:
        return performer_type == PerformerType.REVIEWER

    def generate(self, response: str) -> CodeReviewReport:

        try:
            data = json.loads(response)
            return CodeReviewReport(
                review=data.get("review", ""),
                suggested_code=data.get("suggested_code", ""),
                test_required=data.get("test_required", False)
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response: {e}")


injector = Injector()
review_report_generator = injector.get(ReviewReportGenerator)
