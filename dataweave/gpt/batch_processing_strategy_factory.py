from typing import Dict

from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.enums.product_data_type import BatchDataType
from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.batch_processing_strategy import BatchProcessingStrategy
from dataweave.gpt.batch_processing_strategy_provider import BatchProcessingStrategyProvider, \
    TestCodeProcessingStrategyProvider, ProductProcessingStrategyProvider


@singleton
class BatchProcessingStrategyFactory:

    @inject
    def __init__(self, git_lab_client: GitLabClient, product_hub_client: ProductHubApiClient):
        self.providers: Dict[BatchDataType, BatchProcessingStrategyProvider] = {
            BatchDataType.TEST_CODE: TestCodeProcessingStrategyProvider(git_lab_client),
            BatchDataType.TITLE: ProductProcessingStrategyProvider(product_hub_client),
        }

    def get_strategy(self, data_type: BatchDataType) -> BatchProcessingStrategy:
        if data_type not in self.providers:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self.providers[data_type].provide()

