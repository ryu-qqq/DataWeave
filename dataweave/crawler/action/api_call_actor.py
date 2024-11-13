import json
from typing import Any

from injector import singleton, inject, Injector

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.cache.cursor_cache_manager import CursorCacheManager
from dataweave.crawler.action.action_interface import ActionInterface


## Todo:: API Call Actor에 이제 고도화 시켜야함 어떤 API CALL 프로바이더로 콜할지 현재는 ProductHub만 콜하도록 되어있지만 나중엔 타입별로 처리해야함
@singleton
class ApiCallActor(ActionInterface):

    @inject
    def __init__(self, product_hub_api_client: ProductHubApiClient, cursor_cache_manager: CursorCacheManager):
        self.__product_hub_api_client = product_hub_api_client
        self.__cursor_cache_manager = cursor_cache_manager

    async def action(self, site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                     task: CrawlTaskResponse, data: Any, previous_result: Any):
        site_name = site_context.site_name
        cursor_id = await self.__cursor_cache_manager.get_cursor(site_name)

        page_size = 10
        is_product_group_id_null = json.loads(task.params).get("isProductGroupIdNull", "true") == "true"

        crawl_product_response = self.__product_hub_api_client.fetch_crawl_products_context(
            site_name=site_name,
            page_size=page_size,
            cursor_id=cursor_id,
            is_product_group_id_null=is_product_group_id_null
        )

        if crawl_product_response.cursor is not None:
            await self.__cursor_cache_manager.set_cursor(site_name, crawl_product_response.cursor)

        return crawl_product_response


injector = Injector()
api_call_actor = injector.get(ApiCallActor)

