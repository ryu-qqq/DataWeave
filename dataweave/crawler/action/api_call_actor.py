from typing import Any

from injector import singleton, inject

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.crawler.action.action_interface import ActionInterface


@singleton
class ApiCallActor(ActionInterface):

    @inject
    def __init__(self, product_hub_api_client: ProductHubApiClient):
        self.__product_hub_api_client = product_hub_api_client

    #Todo :: API CALL PROVIDER 또한 고도화 시켜야함 우선 자체 서버 호출용
    async def action(self, site_id: int, site_name: str, data: Any, task: CrawlTaskResponse):
        crawl_product_response = self.__product_hub_api_client.fetch_crawl_products_context(site_name=site_name,
                                                                                            page_size=20,
                                                                                            cursor_id=None)
