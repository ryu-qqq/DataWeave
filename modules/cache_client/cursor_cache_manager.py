from typing import Optional

from injector import singleton, inject, Injector

from modules.cache_client.redis_cache_manager import RedisCacheManager


@singleton
class CursorCacheManager:

    @inject
    def __init__(self, cache_manager: RedisCacheManager):
        self.cache_manager = cache_manager

    async def get_cursor(self, key: str) -> Optional[int]:
        cache_key = f"cursor:{key}"
        cursor_value = await self.cache_manager.get(cache_key)
        return int(cursor_value) if cursor_value else None

    async def set_cursor(self, key: str, cursor_id: int, expire: int = 3600):
        cache_key = f"cursor:{key}"
        await self.cache_manager.set(cache_key, cursor_id, expire=expire)


injector = Injector()
cursor_cache_manager = injector.get(CursorCacheManager)