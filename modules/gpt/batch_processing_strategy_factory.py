from typing import Dict

from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.batch_processing_strategy import BatchProcessingStrategy
from modules.gpt.batch_processing_strategy_provider import BatchProcessingStrategyProvider, \
    TestCodeProcessingStrategyProvider, ProductProcessingStrategyProvider


@singleton
class BatchProcessingStrategyFactory:

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.providers: Dict[BatchDataType, BatchProcessingStrategyProvider] = {
            BatchDataType.TEST_CODE: TestCodeProcessingStrategyProvider(product_hub_client),
            BatchDataType.PRODUCT: ProductProcessingStrategyProvider(product_hub_client),
        }

    def get_strategy(self, data_type: BatchDataType) -> BatchProcessingStrategy:
        if data_type not in self.providers:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self.providers[data_type].provide()


