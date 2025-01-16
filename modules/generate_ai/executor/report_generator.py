from abc import ABC, abstractmethod

from modules.generate_ai.models.open_ai_enums import PerformerType
from modules.generate_ai.models.report import Report


class ReportGenerator(ABC):

    @abstractmethod
    def supports(self, performer_type: PerformerType) -> bool:
        pass

    @abstractmethod
    def generate(self, response: str) -> Report:
        pass
