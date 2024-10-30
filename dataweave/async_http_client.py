from abc import ABCMeta
from typing import Dict, Any, Optional

from dataweave.proxy_manager import ProxyManager
from http_client import HttpClient
from async_session_manager import AsyncSessionManager


class AsyncHttpClient(HttpClient, metaclass=ABCMeta):
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        super().__init__(AsyncSessionManager(), proxy_manager=proxy_manager)

    async def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        session = await self.session_manager.create_session()
        proxies = {"http": self.proxy_manager.get_proxy()} if self.proxy_manager else None
        async with session.request(method, url, headers=headers, proxy=proxies, **kwargs) as response:
            return await response.text() if response.status == 200 else self._handle_response_errors(response, url, 0)