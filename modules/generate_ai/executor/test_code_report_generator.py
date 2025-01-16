import json

from injector import singleton, Injector

from modules.generate_ai.executor.report_generator import ReportGenerator
from modules.generate_ai.models.open_ai_enums import PerformerType
from modules.generate_ai.models.test_review_report import TestCodeReport


@singleton
class TestCodeReportGenerator(ReportGenerator):

    def supports(self, performer_type: PerformerType) -> bool:
        return performer_type == PerformerType.TESTER

    def generate(self, response: str) -> TestCodeReport:

        try:
            data = json.loads(response)
            return TestCodeReport(
                suggested_code=data.get("suggested_code", "")
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response: {e}")


injector = Injector()
test_code_report_generator = injector.get(TestCodeReportGenerator)
