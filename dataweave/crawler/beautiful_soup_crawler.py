from injector import Injector, singleton

from dataweave.crawler.api_crawler_interface import ApiCrawlerInterface


@singleton
class BeautifulSoupCrawler(ApiCrawlerInterface):
    async def crawl_api(self, endpoint: str, method: str, params: dict):
        pass

    async def crawl(self, *args, **kwargs):
        pass


injector = Injector()
beautiful_crawler = injector.get(BeautifulSoupCrawler)
