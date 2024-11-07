import json
from typing import Optional

from injector import singleton, Injector, inject
from dataweave.api_client.models.slice import Slice
from dataweave.api_client.models.product_hub_api_response import ApiResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_response import SiteResponse
from dataweave.api_client.product_hub_config import ProductHubConfig
from dataweave.sync_http_client import SyncHttpClient


@singleton
class ProductHubApiClient:

    @inject
    def __init__(self, config: ProductHubConfig, http_client: SyncHttpClient):
        self.__base_url = config.BASE_URL
        self.__http_client = http_client

    def fetch_sites(self, site_type: Optional[str] = None, cursor_id: Optional[int] = None,
                    page_size: Optional[int] = 20) -> Slice:
        url = f"{self.__base_url}/api/v1/site"
        headers = {"Content-Type": "application/json"}
        params = {"siteType": site_type, "cursorId": cursor_id, "pageSize": page_size}

        response = self.__http_client.request("GET", url, headers=headers, params=params)
        response_data = json.loads(response)

        if "data" in response_data:
            from_dict = Slice.from_dict(response_data["data"], SiteResponse)
            print(from_dict)
            return Slice.from_dict(response_data["data"], SiteResponse)
        else:
            raise ValueError("Unexpected response format")

    def fetch_site_context(self, site_id: int) -> SiteContextResponse:
        url = f"{self.__base_url}/api/v1/site/{site_id}"
        headers = {"Content-Type": "application/json"}

        response = self.__http_client.request("GET", url, headers=headers)
        response_data = json.loads(response)
        api_response = ApiResponse.from_dict(response_data, data_class=SiteContextResponse)
        return api_response.data


injector = Injector()
product_hub_api_client = injector.get(ProductHubApiClient)
