import json
from typing import Dict
from injector import singleton, inject

from dataweave.cache.redis_client import RedisClient


@singleton
class CacheManager:
    @inject
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def get_params(self, site_name: str, endpoint: str, page_key: str = "pageNo", size_key: str = "pageSize") -> \
    Dict[str, int]:
        redis = await self.redis_client.get_redis()
        key = f"{site_name}:{endpoint}"
        cached_data = await redis.get(key)

        if cached_data:
            cached_data = json.loads(cached_data)
            return {
                page_key: cached_data.get(page_key, 0),
                size_key: cached_data.get(size_key, 20)
            }

        return {page_key: 0, size_key: 20}

    async def update_params(self, site_name: str, endpoint: str, page_no: int, page_size: int,
                            dynamic_keys: Dict[str, str]):
        redis = await self.redis_client.get_redis()
        key = f"{site_name}:{endpoint}"
        new_data = {dynamic_keys["page_key"]: page_no, dynamic_keys["size_key"]: page_size}
        await redis.set(key, json.dumps(new_data))
