from dataweave.crawler.api_crawler import ApiCrawler
from dataweave.crawler.selenium_crawler import SeleniumCrawler
from dataweave.crawler.beautiful_soup_crawler import BeautifulSoupCrawler
from dataweave.crawler.crawler_interface import CrawlerInterface
from dataweave.crawler.crawler_type import CrawlerType
from typing import Dict, Type



class CrawlerProvider:
    def __init__(self):

        self._crawlers: Dict[CrawlerType, Type[CrawlerInterface]] = {
            CrawlerType.API: ApiCrawler,
            CrawlerType.SELENIUM: SeleniumCrawler,
            CrawlerType.BEAUTIFUL_SOUP: BeautifulSoupCrawler,
        }

    def get_crawler(self, crawl_type: CrawlerType, **kwargs) -> CrawlerInterface:
        if crawl_type not in self._crawlers:
            raise ValueError(f"지원되지 않는 크롤링 타입입니다: {crawl_type}")

        # 크롤러 클래스 선택 후 인스턴스 생성
        crawler_class = self._crawlers[crawl_type]
        return crawler_class(**kwargs)