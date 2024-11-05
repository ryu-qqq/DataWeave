from abc import abstractmethod

from dataweave.crawler.crawler_interface import CrawlerInterface


class ApiCrawlerInterface(CrawlerInterface):
    @abstractmethod
    async def crawl_api(self, *args, **kwargs):
        """Crawls using an API endpoint and optional parameters."""
        pass
