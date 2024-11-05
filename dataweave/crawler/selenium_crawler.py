from injector import Injector, singleton

from dataweave.crawler.api_crawler_interface import ApiCrawlerInterface


@singleton
class SeleniumCrawler(ApiCrawlerInterface):
    async def crawl_api(self, endpoint: str, method: str, params: dict):
        pass

    async def crawl(self, *args, **kwargs):
        pass


injector = Injector()
selenium_crawler = injector.get(SeleniumCrawler)
