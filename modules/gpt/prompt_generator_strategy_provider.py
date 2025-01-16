from abc import abstractmethod, ABC

from modules.gpt.prompt_generator import PromptGenerator


class PromptGeneratorStrategyProvider(ABC):

    @abstractmethod
    def provide(self) -> PromptGenerator:
        pass
