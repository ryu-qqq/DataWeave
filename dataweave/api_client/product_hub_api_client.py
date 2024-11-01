import json

from injector import singleton, Injector, inject

from dataweave.api_client.models.product_hub_api_response import ApiResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.product_hub_config import ProductHubConfig
from dataweave.sync_http_client import SyncHttpClient


@singleton
class ProductHubApiClient:

    @inject
    def __init__(self, config: ProductHubConfig, http_client: SyncHttpClient):
        self.__base_url = config.BASE_URL
        self.__http_client = http_client

    def fetch_site_context(self, site_id: int) -> SiteContextResponse:
        url = f"{self.__base_url}/api/v1/site/{site_id}"
        headers = {"Content-Type": "application/json"}

        response_text = self.__http_client.request("GET", url, headers=headers)
        response_data = json.loads(response_text)
        api_response = ApiResponse.from_dict(response_data, data_class=SiteContextResponse)
        return api_response.data


injector = Injector()
product_hub_api_client = injector.get(ProductHubApiClient)
