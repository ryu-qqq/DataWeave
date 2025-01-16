from typing import Dict

from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.data_fetcher_strategy import DataFetcherStrategy
from modules.gpt.data_fetcher_strategy_provider import DataFetcherStrategyProvider, GitEventFetcherStrategyProvider, \
    ProductDataFetcherStrategyProvider


@singleton
class DataFetcherStrategyFactory:

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.providers: Dict[BatchDataType, DataFetcherStrategyProvider] = {
            BatchDataType.TEST_CODE: GitEventFetcherStrategyProvider(product_hub_client),
            BatchDataType.PRODUCT: ProductDataFetcherStrategyProvider(product_hub_client),
        }

    def get_strategy(self, batch_data_type: BatchDataType) -> DataFetcherStrategy:
        if batch_data_type not in self.providers:
            raise ValueError(f"Unsupported batch data type: {batch_data_type}")
        return self.providers[batch_data_type].provide()


