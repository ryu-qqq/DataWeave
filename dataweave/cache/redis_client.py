import aioredis
from injector import singleton, inject

from dataweave.cache.redis_config import RedisConfig


@singleton
class RedisClient:
    @inject
    def __init__(self, redis_config: RedisConfig):
        self.redis_config = redis_config
        self._redis = None

    async def get_redis(self):
        if self._redis is None:
            self._redis = await aioredis.from_url(
                f"redis://{self.redis_config.REDIS_HOST}:{self.redis_config.REDIS_PORT}/{self.redis_config.REDIS_DB}"
            )
        return self._redis

    async def close(self):
        if self._redis:
            await self._redis.close()
