from typing import Dict

from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.enums.source_type import SourceType
from dataweave.gpt.data_fetcher_strategy import DataFetcherStrategy
from dataweave.gpt.data_fetcher_strategy_provider import DataFetcherStrategyProvider, GitEventFetcherStrategyProvider, \
    ProductDataFetcherStrategyProvider


@singleton
class DataFetcherStrategyFactory:

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.providers: Dict[SourceType, DataFetcherStrategyProvider] = {
            SourceType.TEST_CODE: GitEventFetcherStrategyProvider(product_hub_client),
            SourceType.PRODUCT: ProductDataFetcherStrategyProvider(product_hub_client),
        }

    def get_strategy(self, source_type: SourceType) -> DataFetcherStrategy:
        if source_type not in self.providers:
            raise ValueError(f"Unsupported source type: {source_type}")
        return self.providers[source_type].provide()


