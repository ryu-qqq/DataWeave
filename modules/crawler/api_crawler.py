import logging
import re
from typing import Dict

from injector import Injector, singleton, inject

from modules.http_client.async_http_client import AsyncHttpClient
from modules.crawler.api_crawler_interface import ApiCrawlerInterface
from modules.crawler.page_cache_manager import PageCacheManager
from modules.crawler.parser.api_response_parser import ApiResponseParser


@singleton
class ApiCrawler(ApiCrawlerInterface):

    @inject
    def __init__(self, http_client: AsyncHttpClient, page_cache_manager: PageCacheManager):
        self.http_client = http_client
        self.page_cache_manager = page_cache_manager

    @staticmethod
    def extract_dynamic_keys(parameters: str) -> Dict[str, str]:
        keys = re.findall(r'(\w+)={}', parameters)
        return {"page_key": keys[0], "size_key": keys[1]} if len(keys) >= 2 else {"page_key": "pageNo",
                                                                                  "size_key": "pageSize"}

    async def crawl_api(self, site_name: str, base_url: str, endpoint: str, parameters: str, method: str,
                        headers: Dict[str, str], response_mapping: str):
        headers = headers or {"Content-Type": "application/json"}
        logging.info(f"Using headers: {headers}")

        cached_params = {"pageNo": 0, "pageSize": 20 }

        if parameters:
            dynamic_keys = self.extract_dynamic_keys(parameters)
            cached_params = await self.page_cache_manager.get_params(site_name, endpoint, dynamic_keys["page_key"], dynamic_keys["size_key"])
            resolved_parameters = parameters.format(cached_params[dynamic_keys["page_key"]], cached_params[dynamic_keys["size_key"]])
        else:
            resolved_parameters = parameters

        url = f"{base_url}{endpoint}?{resolved_parameters}" if resolved_parameters else f"{base_url}{endpoint}"
        response = await self.http_client.request(method=method, url=url, headers=headers)

        parser = ApiResponseParser(response_mapping)
        parsed_data = parser.parse_response(response)

        if parameters:
            if not parsed_data:
                await self.page_cache_manager.update_params(site_name, endpoint, page_no=0,
                                                       page_size=cached_params[dynamic_keys["size_key"]],
                                                       dynamic_keys=dynamic_keys)
            else:
                await self.page_cache_manager.update_params(site_name, endpoint,
                                                       page_no=cached_params[dynamic_keys["page_key"]] + 1,
                                                       page_size=cached_params[dynamic_keys["size_key"]],
                                                       dynamic_keys=dynamic_keys)

        return parsed_data

    async def crawl(self, *args, **kwargs):
        return await self.crawl_api(*args, **kwargs)


injector = Injector()
api_crawler = injector.get(ApiCrawler)
