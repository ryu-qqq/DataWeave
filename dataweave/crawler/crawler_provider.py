from dataweave.crawler.api_crawler import api_crawler
from dataweave.crawler.selenium_crawler import selenium_crawler
from dataweave.crawler.beautiful_soup_crawler import beautiful_crawler
from dataweave.crawler.crawler_interface import CrawlerInterface
from dataweave.enums.crawler_type import CrawlerType


class CrawlerProvider:

    @staticmethod
    def get_crawler(crawl_type: str) -> CrawlerInterface:
        if crawl_type == CrawlerType.API.name:
            return api_crawler
        elif crawl_type == CrawlerType.SELENIUM.name:
            return selenium_crawler
        elif crawl_type == CrawlerType.BEAUTIFUL_SOUP.name:
            return beautiful_crawler

        raise ValueError(f"Unsupported Crawl type: {crawl_type}")
