import logging
from typing import Optional, Any, List

from injector import inject, singleton, Injector

from modules.cache_client.cache_manager import CacheManager
from modules.cache_client.redis_client import RedisClient


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

    async def scan(self, pattern: str, count: int = 100) -> List[str]:
        redis = await self._redis_client.get_redis()
        cursor = 0  # 초기 커서 값
        keys = []

        while True:
            logging.info(f"Starting SCAN with cursor: {cursor}")
            cursor, batch_keys = await redis.scan(cursor=cursor, match=pattern, count=count)

            logging.info(f"SCAN returned cursor: {cursor}, batch_keys: {batch_keys}")
            keys.extend(batch_keys)

            if cursor == 0:  # 커서가 0이면 루프 종료
                break

        logging.info(f"Total keys found: {keys}")
        return [key.decode('utf-8') for key in keys]


injector = Injector()
redis_cache_manager = injector.get(RedisCacheManager)
