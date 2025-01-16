from abc import abstractmethod

from modules.crawler.crawler_interface import CrawlerInterface


class DynamicPageCrawlerInterface(CrawlerInterface):
    @abstractmethod
    async def crawl_dynamic_page(self, url: str, actions: list):
        """Crawls a dynamic page with actions like clicks or scrolls."""
        pass
