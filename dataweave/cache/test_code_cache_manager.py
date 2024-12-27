import json
from typing import List

from injector import singleton, inject

from dataweave.cache.redis_cache_manager import RedisCacheManager
from dataweave.enums.batch_status import BatchStatus


@singleton
class TestCodeCacheManager:

    @inject
    def __init__(self, cache_manager: RedisCacheManager):
        self.__cache_manager = cache_manager

    async def initialize_commit(self, commit_id: str, class_name: str, methods: List[str]):

        key = f"commit:{commit_id}"
        data = await self.__cache_manager.get(key)
        if data:
            cache_data = json.loads(data)
        else:
            cache_data = {}

        if class_name not in cache_data:
            cache_data[class_name] = {method: {"status": BatchStatus.PENDING.name} for method in methods}

        await self.__cache_manager.set(key, json.dumps(cache_data))

    async def update_method_status(self, commit_id: str, class_name: str, method_name: str, status: BatchStatus,
                                   test_code: str = None):

        key = f"commit:{commit_id}"
        data = await self.__cache_manager.get(key)
        if not data:
            raise ValueError(f"No data found for commit {commit_id}")

        cache_data = json.loads(data)
        if class_name in cache_data and method_name in cache_data[class_name]:
            cache_data[class_name][method_name]["status"] = status.name
            if test_code:
                cache_data[class_name][method_name]["test_code"] = test_code

            await self.__cache_manager.set(key, json.dumps(cache_data))

    async def get_class_status(self, commit_id: str, class_name: str):
        key = f"commit:{commit_id}"
        data = await self.__cache_manager.get(key)
        if not data:
            return None

        cache_data = json.loads(data)
        return cache_data.get(class_name)

    async def is_class_completed(self, commit_id: str, class_name: str) -> bool:
        class_status = await self.get_class_status(commit_id, class_name)
        if not class_status:
            return False

        return all(method["status"] == BatchStatus.COMPLETED.name for method in class_status.values())