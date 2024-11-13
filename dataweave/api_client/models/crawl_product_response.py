
class CrawlProductResponse:
    def __init__(self, crawl_product_id: int, site_id: int, site_name: str, site_product_id: str, product_name: str, product_group_id: int):
        self.crawl_product_id = crawl_product_id
        self.site_id = site_id
        self.site_name = site_name
        self.site_product_id = site_product_id
        self.product_name = product_name
        self.product_group_id = product_group_id


    @staticmethod
    def from_dict(data: dict) -> 'CrawlProductResponse':
        return CrawlProductResponse(
            crawl_product_id= data.get("crawlProductId"),
            site_id=data.get("siteId"),
            site_name=data.get("siteName"),
            site_product_id=data.get("siteProductId"),
            product_name=data.get("productName"),
            product_group_id=data.get("productGroupId")
        )
