from injector import Injector, singleton

from dataweave.crawler.html_crawler_interface import HtmlCrawlerInterface


@singleton
class BeautifulSoupCrawler(HtmlCrawlerInterface):

    async def crawl_html(self, *args, **kwargs):
        pass

    async def crawl(self, *args, **kwargs):
        return self.crawl_html(*args, **kwargs)


injector = Injector()
beautiful_crawler = injector.get(BeautifulSoupCrawler)
