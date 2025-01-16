from abc import ABC, abstractmethod


class Prompter(ABC):
    @abstractmethod
    def generate_prompt(self, code: str) -> str:
        pass
