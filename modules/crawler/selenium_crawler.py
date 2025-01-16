from injector import Injector, singleton

from modules.crawler.dynamic_page_crawler_interface import DynamicPageCrawlerInterface


@singleton
class SeleniumCrawler(DynamicPageCrawlerInterface):
    async def crawl_dynamic_page(self, url: str, actions: list):
        pass

    async def crawl(self, *args, **kwargs):
        return self.crawl_dynamic_page(*args, **kwargs)


injector = Injector()
selenium_crawler = injector.get(SeleniumCrawler)
