from typing import List, Optional

from modules.generate_ai.executor.code_review_report_generator import review_report_generator
from modules.generate_ai.executor.report_generator import ReportGenerator
from modules.generate_ai.executor.test_code_report_generator import test_code_report_generator
from modules.generate_ai.models.open_ai_enums import PerformerType


class ReportGeneratorProvider:

    def __init__(self, generators: List[ReportGenerator]):
        self.generators = generators

    def get_generator(self, performer_type: PerformerType) -> Optional[ReportGenerator]:
        for generator in self.generators:
            if generator.supports(performer_type):
                return generator
        return None


report_generator_provider = ReportGeneratorProvider(generators=[review_report_generator, test_code_report_generator])