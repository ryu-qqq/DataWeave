from abc import abstractmethod

from dataweave.crawler.crawler_interface import CrawlerInterface


class HtmlCrawlerInterface(CrawlerInterface):
    @abstractmethod
    async def crawl_html(self, *args, **kwargs):
        """Crawls an HTML page at the given URL and parses data."""
        pass
