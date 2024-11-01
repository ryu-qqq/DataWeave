from abc import abstractmethod

from dataweave.crawler.crawler_interface import CrawlerInterface


class ApiCrawlerInterface(CrawlerInterface):
    @abstractmethod
    async def crawl_api(self, endpoint: str, method: str, params: dict):
        """Crawls using an API endpoint and optional parameters."""
        pass
