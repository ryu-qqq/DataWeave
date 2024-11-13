from typing import Optional

from injector import singleton, inject

from dataweave.cache.redis_cache_manager import RedisCacheManager

@singleton
class CursorCacheManager:

    @inject
    def __init__(self, cache_manager: RedisCacheManager):
        self.cache_manager = cache_manager

    async def get_cursor(self, site_name: str) -> Optional[int]:
        cache_key = f"cursor:{site_name}"
        cursor_value = await self.cache_manager.get(cache_key)
        return int(cursor_value) if cursor_value else None

    async def set_cursor(self, site_name: str, cursor_id: int, expire: int = 3600):
        cache_key = f"cursor:{site_name}"
        await self.cache_manager.set(cache_key, cursor_id, expire=expire)
