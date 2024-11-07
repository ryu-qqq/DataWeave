from abc import ABC, abstractmethod
from typing import Optional, Any


class CacheManager(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        pass

    @abstractmethod
    async def set_expire(self, key: str, time: int) -> bool:
        pass
