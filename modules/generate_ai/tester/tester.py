from abc import abstractmethod, ABC

from modules.generate_ai.models.code import Code
from modules.generate_ai.prompter.prompter import Prompter


class Tester(ABC):

    def __init__(self, prompter: Prompter):
        self._prompter = prompter

    @abstractmethod
    def supports(self, code: Code) -> bool:
        pass

    @abstractmethod
    def write_tests(self, code: str) -> str:
        pass
