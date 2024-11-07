from typing import Optional, Any

from injector import inject, singleton, Injector

from dataweave.cache.cache_manager import CacheManager
from dataweave.cache.redis_client import RedisClient


@singleton
class RedisCacheManager(CacheManager):
    @inject
    def __init__(self, redis_client: RedisClient):
        self._redis_client = redis_client

    async def get(self, key: str) -> Optional[str]:
        redis = await self._redis_client.get_redis()
        value = await redis.get(key)
        return value.decode('utf-8') if value else None

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        redis = await self._redis_client.get_redis()
        await redis.set(key, str(value))
        if expire is not None:
            await redis.expire(key, expire)

    async def exists(self, key: str) -> bool:
        redis = await self._redis_client.get_redis()
        return await redis.exists(key) > 0

    async def delete(self, key: str) -> None:
        redis = await self._redis_client.get_redis()
        await redis.delete(key)

    async def increment(self, key: str, amount: int = 1) -> int:
        redis = await self._redis_client.get_redis()
        return await redis.incrby(key, amount)

    async def set_expire(self, key: str, time: int) -> bool:
        redis = await self._redis_client.get_redis()
        return await redis.expire(key, time)


injector = Injector()
redis_cache_manager = injector.get(RedisCacheManager)
