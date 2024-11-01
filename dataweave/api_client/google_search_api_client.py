import json

from injector import singleton, inject, Injector

from dataweave.api_client.google_search_config import GoogleSearchConfig
from dataweave.api_client.models.google_search_response import GoogleSearchResponse
from dataweave.async_http_client import AsyncHttpClient


@singleton
class GoogleSearchApiClient:

    @inject
    def __init__(self, config: GoogleSearchConfig, http_client: AsyncHttpClient):
        self.__url = config.URL
        self.__http_client = http_client

    async def fetch_search_word_results(self, search_word: str) -> GoogleSearchResponse:
        url = f"{self.__url}{search_word} "
        headers = {"Content-Type": "application/json"}

        response_text = await self.__http_client.request("GET", url, headers=headers)
        response_data = json.loads(response_text)
        print(response_data)

        return None


injector = Injector()
google_search_api_client = injector.get(GoogleSearchApiClient)
