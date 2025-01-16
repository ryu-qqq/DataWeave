from abc import ABC, abstractmethod
from typing import Optional


class ProxyManager(ABC):
    """Interface for managing proxies. Create your custom proxy manager
    implementation based on the desired proxy service or provider."""

    @abstractmethod
    def get_proxy(self) -> Optional[str]:
        """Returns a proxy URL or None if no proxy is to be used."""
        pass
