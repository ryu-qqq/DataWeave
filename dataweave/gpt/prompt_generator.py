from abc import ABC, abstractmethod
from typing import List

from dataweave.gpt.prompt import Prompt


class PromptGenerator(ABC):
    @abstractmethod
    async def get_prompt(self, *args, **kwargs) -> List[Prompt]:
        pass
