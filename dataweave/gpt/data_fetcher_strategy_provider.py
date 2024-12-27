from abc import abstractmethod, ABC

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.gpt.data_fetcher_strategy import DataFetcherStrategy, GitEventFetcherStrategy, ProductDataFetcherStrategy


class DataFetcherStrategyProvider(ABC):
    @abstractmethod
    def provide(self) -> DataFetcherStrategy:
        pass


class GitEventFetcherStrategyProvider(DataFetcherStrategyProvider):
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.product_hub_client = product_hub_client

    def provide(self) -> DataFetcherStrategy:
        return GitEventFetcherStrategy(self.product_hub_client)


class ProductDataFetcherStrategyProvider(DataFetcherStrategyProvider):
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.product_hub_client = product_hub_client

    def provide(self) -> DataFetcherStrategy:
        return ProductDataFetcherStrategy(self.product_hub_client)
