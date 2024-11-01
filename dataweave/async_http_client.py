from typing import Dict, Any, Optional

from dataweave.async_session_manager import AsyncSessionManager
from dataweave.proxy_manager import ProxyManager
from dataweave.http_client import HttpClient


class AsyncHttpClient(HttpClient):
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        super().__init__(AsyncSessionManager(), proxy_manager=proxy_manager)

    async def initialize_session(self):
        self.session = await self.session_manager.create_session()

    async def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        if not self.session:
            await self.initialize_session()
        proxies = {"http": self.proxy_manager.get_proxy()} if self.proxy_manager else None
        async with self.session.request(method, url, headers=headers, proxy=proxies, **kwargs) as response:
            return await response.text() if response.status == 200 else self._handle_response_errors(response, url, 0)

