import json
from typing import Any, List

from injector import singleton, inject
from jsonpath_ng import parse

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.cache.cache_manager import CacheManager
from dataweave.crawler.action.action_interface import ActionInterface


@singleton
class SaveCacheActor(ActionInterface):

    @inject
    def __init__(self, cache_manager: CacheManager):
        self.__cache_manager = cache_manager

    async def action(self, site_id: int, site_name: str, data: Any, task: CrawlTaskResponse):
        params = json.loads(task.params)
        key_field = params.get("key")
        value_field = params.get("value")

        response_mapping = json.loads(task.response_mapping)
        main_key, jsonpath_expression = next(iter(response_mapping.items()))
        jsonpath_expr = parse(jsonpath_expression)

        extracted_items = [match.value for match in jsonpath_expr.find(data)]

        for item in extracted_items:
            key_value = item.get(key_field)
            value = item.get(value_field)
            if key_value is not None and value is not None:
                cache_key = f"{site_name}:{task.target}:{key_value}"
                if not await self.__cache_manager.exists(cache_key):
                    await self.__cache_manager.set(cache_key, value)

