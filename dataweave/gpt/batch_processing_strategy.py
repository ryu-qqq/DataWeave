from abc import ABC, abstractmethod
from dataweave.gpt.batch_models import Batch


class BatchProcessingStrategy(ABC):
    @abstractmethod
    async def process_batch(self, batch: Batch, save_path: str) -> list:
        pass
