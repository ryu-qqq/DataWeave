from abc import ABC, abstractmethod
from typing import List, Any

from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient


class DataFetcherStrategy(ABC):
    @abstractmethod
    def fetch_data(self, **kwargs) -> Any:
        pass


@singleton
class GitEventFetcherStrategy(DataFetcherStrategy):

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.__product_hub_client = product_hub_client

    def fetch_data(self, status: str, change_types: List[str], page_size: int, page_number: int, cursor: int,
                   sort: str):
        return self.__product_hub_client.fetch_git_events(
            status=status,
            change_types=change_types,
            page_size=page_size,
            page_number=page_number,
            cursor=cursor,
            sort=sort
        ).content


@singleton
class ProductDataFetcherStrategy(DataFetcherStrategy):

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.__product_hub_client = product_hub_client

    def fetch_data(self, seller_id: int, cursor: int, status: str, page_size: int):
        return self.__product_hub_client.fetch_product_group_processing_data(
            seller_id=seller_id,
            cursor=cursor,
            status=status,
            page_size=page_size
        ).content