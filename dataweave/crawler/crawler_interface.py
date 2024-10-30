import asyncio
from typing import Optional

import aiohttp

from abc import abstractmethod, ABC, ABCMeta
from dataweave.cookie_manager import CookieManager
from dataweave.http_client import HttpClient
from dataweave.proxy_manager import ProxyManager


class CrawlerInterface(ABC):
    @abstractmethod
    async def crawl(self, *args, **kwargs):
        pass


class BaseCrawler(CrawlerInterface, metaclass=ABCMeta):
    def __init__(self, proxy_manager: Optional[ProxyManager], cookie_manager: CookieManager, http_client: HttpClient, headers=None,
                 timeout=None):
        self.session = None
        self.headers = headers if headers is not None else {}
        self.__proxy_manager = proxy_manager
        self.__cookie_manager = cookie_manager
        self.__http_client = http_client
        self.timeout = timeout or aiohttp.ClientTimeout(total=60)

    async def __aenter__(self):
        await self.initialize_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close_resources()

    async def initialize_session(self):
        if self.session is None:
            proxy_url = self.__proxy_manager.get_proxy() if self.__proxy_manager else None
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                headers=self.headers,
                timeout=self.timeout
            )

    async def close_resources(self):
        if self.session:
            await self.session.close()
            self.session = None

    def get_cookie_manager(self):
        return self.__cookie_manager

    def get_proxy_manager(self):
        return self.__proxy_manager

    def get_http_client(self):
        return self.__http_client

    @abstractmethod
    async def crawl(self, *args, **kwargs):
        pass

    def run_async(self, coroutine):
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            return loop.run_until_complete(coroutine)
        else:
            return asyncio.ensure_future(coroutine)