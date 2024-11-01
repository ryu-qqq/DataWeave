class CrawlSettingResponse:
    def __init__(self, crawl_frequency: int, crawl_type: str):
        self.crawl_frequency = crawl_frequency
        self.crawl_type = crawl_type

    @staticmethod
    def from_dict(data: dict) -> 'CrawlSettingResponse':
        return CrawlSettingResponse(
            crawl_frequency=data.get("crawlFrequency"),
            crawl_type=data.get("crawlType")
        )