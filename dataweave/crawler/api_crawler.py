from typing import Dict, Optional

from dataweave.async_http_client import AsyncHttpClient
from dataweave.crawler.api_crawler_interface import ApiCrawlerInterface
from dataweave.crawler.parser.api_response_parser import ApiResponseParser
from dataweave.crawler.parser.custon_reponse_parser import CustomResponseParser


class ApiCrawler(ApiCrawlerInterface):

    def __init__(self, http_client: AsyncHttpClient, response_mapping: Optional[str] = None,
                 parser: Optional[CustomResponseParser] = None):
        self.http_client = http_client
        self.parser = parser if parser else ApiResponseParser(response_mapping)

    async def crawl_api(self, endpoint: str, method: str, params: Dict[str, str], headers: Dict[str, str] = None):
        headers = headers or {"Content-Type": "application/json"}

        response_text = await self.http_client.request(
            method=method,
            url=endpoint,
            headers=headers,
            params=params
        )

        parsed_data = self.parser.parse_response(response_text)
        return parsed_data

    async def crawl(self, *args, **kwargs):
        return await self.crawl_api(*args, **kwargs)
