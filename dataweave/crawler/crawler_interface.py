from abc import abstractmethod, ABC


class CrawlerInterface(ABC):
    @abstractmethod
    async def crawl(self, *args, **kwargs):
        pass
