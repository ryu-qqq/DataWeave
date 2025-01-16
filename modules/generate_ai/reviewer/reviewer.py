from abc import ABC, abstractmethod

from modules.generate_ai.models.code import Code
from modules.generate_ai.prompter.prompter import Prompter


# 추상화: 리뷰어
class Reviewer(ABC):

    def __init__(self, prompter: Prompter):
        self._prompter = prompter

    @abstractmethod
    def supports(self, code: Code) -> bool:
        pass

    @abstractmethod
    def review_code(self, code: Code) -> str:
        pass