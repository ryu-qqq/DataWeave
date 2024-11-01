from dataweave.crawler.api_crawler_interface import ApiCrawlerInterface


class SeleniumCrawler(ApiCrawlerInterface):
    async def crawl_api(self, endpoint: str, method: str, params: dict):
        pass

    async def crawl(self, *args, **kwargs):
        pass