from abc import ABC, abstractmethod

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.batch_processing_strategy import BatchProcessingStrategy
from dataweave.gpt.product_processing_strategy import ProductProcessingStrategy
from dataweave.gpt.test_code_processing_strategy import TestCodeProcessingStrategy


class BatchProcessingStrategyProvider(ABC):
    @abstractmethod
    def provide(self) -> BatchProcessingStrategy:
        pass


class TestCodeProcessingStrategyProvider(BatchProcessingStrategyProvider):
    def __init__(self, gitlab_client: GitLabClient):
        self.gitlab_client = gitlab_client

    def provide(self) -> BatchProcessingStrategy:
        return TestCodeProcessingStrategy(self.gitlab_client)


class ProductProcessingStrategyProvider(BatchProcessingStrategyProvider):
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.product_hub_client = product_hub_client

    def provide(self) -> BatchProcessingStrategy:
        return ProductProcessingStrategy(self.product_hub_client)
