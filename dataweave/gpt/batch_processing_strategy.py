from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from dataweave.gpt.models.batch_models import Batch
from dataweave.gpt.models.prompt_models import PromptMetadata

T = TypeVar("T", bound=PromptMetadata)


class BatchProcessingStrategy(ABC, Generic[T]):
    @abstractmethod
    async def process(self, batch: Batch[T]):
        pass
