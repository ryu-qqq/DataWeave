from abc import abstractmethod, ABC

from dataweave.gpt.prompt_generator import PromptGenerator


class PromptGeneratorStrategyProvider(ABC):
    @abstractmethod
    def provide(self) -> PromptGenerator:
        pass
