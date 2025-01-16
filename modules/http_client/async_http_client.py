import logging
from typing import Dict, Any, Optional

from modules.http_client.async_session_manager import AsyncSessionManager
from modules.http_client.client_exception import UnauthorizedException, ForbiddenException, TooManyRequestException, \
    UnExpectedException
from modules.http_client.proxy_manager import ProxyManager
from modules.http_client.http_client import HttpClient


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
            return await response.text() if response.status == 200 else await self._handle_response_errors(response, url, 0)

    async def request_response(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        if not self.session:
            await self.initialize_session()
        proxies = {"http": self.proxy_manager.get_proxy()} if self.proxy_manager else None
        async with self.session.request(method, url, headers=headers, proxy=proxies, **kwargs) as response:
            return response if response.status == 200 else self._handle_response_errors(response, url, 0)

    async def _handle_response_errors(self, response, url: str, attempt: int) -> Optional[str]:
        text = await response.text()
        status = response.status

        if status == 401:
            logging.error(f"Unauthorized (401) error for {url}. Check your credentials.")
            raise UnauthorizedException("Token expired, fetching new token.")
        elif status == 403:
            logging.error(f"Forbidden (403) error for {url}. Check your permissions.")
            raise ForbiddenException("Token expired, fetching new token.")
        elif status == 429:
            logging.error(f"Too Many Requests (429). Retrying {url} after backoff.")
            raise TooManyRequestException("Too Many Requests (429)")
        elif status == 200:
            return text
        else:
            logging.error(f"Received status {status} from {url}: {text}")
            raise UnExpectedException("UnExpected Error")