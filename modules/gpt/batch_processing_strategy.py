from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from modules.gpt.models.batch_models import Batch
from modules.gpt.models.prompt_models import PromptMetadata

T = TypeVar("T", bound=PromptMetadata)


class BatchProcessingStrategy(ABC, Generic[T]):
    @abstractmethod
    async def process(self, batch: Batch[T]):
        pass
