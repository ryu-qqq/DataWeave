import json
from typing import Optional, Dict, Any, List

from injector import singleton, Injector, inject

from dataweave.api_client.models.crawl_product_response import CrawlProductResponse
from dataweave.api_client.models.git_event_context_response import GitEventContextResponse
from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse
from dataweave.api_client.models.product_hub_api_response import ApiResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_response import SiteResponse
from dataweave.api_client.models.slice import Slice
from dataweave.api_client.product_hub_config import ProductHubConfig
from dataweave.gpt.batch_product_models import BatchProductModel
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

    def fetch_crawl_products_context(self, site_name: str, page_size: int, is_product_group_id_null: bool,
                                     cursor_id: Optional[int]) -> Slice:
        url = f"{self.__base_url}/api/v1/site/crawl/product"
        headers = {"Content-Type": "application/json"}

        params = {"siteName": site_name, "isProductGroupIdNull": is_product_group_id_null, "cursorId": cursor_id,
                  "pageSize": page_size}
        response = self.__http_client.request("GET", url, headers=headers, params=params)

        response_data = json.loads(response)

        if "data" in response_data:
            return Slice.from_dict(response_data["data"], CrawlProductResponse)
        else:
            raise ValueError("Unexpected response format")

    def fetch_product_group_processing_data(self, seller_id: int, cursor: int, status: str, page_size: int) -> Slice:

        url = f"{self.__base_url}/api/v1/product/processing-waiting"
        headers = {"Content-Type": "application/json"}
        params = {"sellerId": seller_id, "productStatus": status, "cursorId": cursor, "pageSize": page_size}
        response = self.__http_client.request("GET", url, headers=headers, params=params)

        response_data = json.loads(response)

        if "data" in response_data:
            return Slice.from_dict(response_data["data"], GptTrainingDataResponse)
        else:
            raise ValueError("Unexpected response format")

    def update_processing_products(self, processed_data: BatchProductModel):
        url = f"{self.__base_url}/api/v1/product/processing-completed"
        headers = {"Content-Type": "application/json"}

        request_body = self._convert_to_camel_case(processed_data)
        self.__http_client.request("POST", url, headers=headers, data=json.dumps(request_body))

    def fetch_git_events(self, status: str, change_types: List[str], page_size: int, page_number: int, cursor: int,
                         sort: str) -> Slice:

        url = f"{self.__base_url}/api/v1/git-events"
        headers = {"Content-Type": "application/json"}
        params = {"gitEventStatus": status, "change_types": change_types, "pageSize": page_size,
                  "pageNumber": page_number, "cursorId": cursor, "sort": sort}
        response = self.__http_client.request("GET", url, headers=headers, params=params)

        response_data = json.loads(response)

        if "data" in response_data:
            return Slice.from_dict(response_data["data"], GitEventContextResponse)
        else:
            raise ValueError("Unexpected response format")

    def _convert_to_camel_case(self, processed_datas: BatchProductModel) -> dict:
        serialized_data = processed_datas.to_dict()
        return self._to_camel_case_dict(serialized_data)

    def _to_camel_case_dict(self, snake_case_dict: Dict[str, Any]) -> Dict[str, Any]:
        camel_case_dict = {}
        for key, value in snake_case_dict.items():
            camel_case_key = self._to_camel_case(key)
            camel_case_dict[camel_case_key] = value
        return camel_case_dict

    @staticmethod
    def _to_camel_case(snake_str: str) -> str:
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])


injector = Injector()
product_hub_api_client = injector.get(ProductHubApiClient)
