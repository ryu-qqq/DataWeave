import json
import logging
from typing import Optional, List

from injector import singleton, inject

from dataweave.cache.redis_cache_manager import RedisCacheManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.processor.batch_models import Batch


@singleton
class BatchIdManager:

    @inject
    def __init__(self, cache_manager: RedisCacheManager):
        self.__cache_manager = cache_manager
        self.__namespace = "batch_id"

    def _generate_key(self, batch_id: str) -> str:
        return f"{self.__namespace}:{batch_id}"

    async def save_batch(self, batch: Batch, expire: Optional[int] = None) -> None:
        key = self._generate_key(batch.batch_id)
        value = json.dumps(batch.to_dict())
        await self.__cache_manager.set(key, value, expire)
        logging.info(f"Batch '{batch.batch_id}' saved in Cache with status '{batch.status}'")

    async def delete_batch(self, batch: Batch) -> None:
        await self.__cache_manager.delete(batch.batch_id)
        logging.info(f"Batch '{batch.batch_id}' deleted in Cache with status '{batch.status}'")

    async def get_batch(self, batch_id: str) -> Optional[Batch]:
        key = self._generate_key(batch_id)
        data = await self.__cache_manager.get(key)
        if isinstance(data, str):
            data = json.loads(data)
        if data:
            return Batch(**data)
        return None

    async def update_batch_status(self, batch: Batch, status: BatchStatus) -> None:
        existing_batch = await self.get_batch(batch.batch_id)
        if existing_batch:
            existing_batch.update_status(status)
            existing_batch.data = batch.data
            await self.save_batch(existing_batch)
            logging.info(f"Batch '{batch.batch_id}' updated to status '{status}' with additional data: {batch.data}")
        else:
            logging.warning(f"Batch '{batch.batch_id}' not found for status update")

    async def batch_exists(self, batch_id: str) -> bool:
        key = self._generate_key(batch_id)
        return await self.__cache_manager.exists(key)

    async def list_batches_by_status(self, status: BatchStatus) -> List[Batch]:
        pattern = f"{self.__namespace}:*"
        keys = await self.__cache_manager.scan(pattern=pattern, count=10)
        batches = []

        for key in keys:
            data = await self.__cache_manager.get(key)
            if isinstance(data, str):
                data = json.loads(data)
            batch = Batch(**data)
            if batch.status == status.name:
                batches.append(batch)

        return batches
