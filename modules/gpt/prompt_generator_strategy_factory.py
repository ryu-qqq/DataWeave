from typing import Dict

from injector import singleton, inject

from modules.git_lab.git_lab_client import GitLabClient
from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.product_prompt_generator import ProductPromptGenerator
from modules.gpt.prompt_generator import PromptGenerator
from modules.gpt.prompt_generator_strategy_provider import PromptGeneratorStrategyProvider
from modules.gpt.test_code_prompt_generator import TestCodePromptGenerator


class TestCodePromptGeneratorStrategyProvider(PromptGeneratorStrategyProvider):
    def __init__(self, gitlab_client: GitLabClient):
        self.gitlab_client = gitlab_client

    def provide(self) -> PromptGenerator:
        return TestCodePromptGenerator(self.gitlab_client)


class ProductPromptGeneratorStrategyProvider(PromptGeneratorStrategyProvider):
    def provide(self) -> PromptGenerator:
        return ProductPromptGenerator()


@singleton
class PromptGeneratorFactory:

    @inject
    def __init__(self, gitlab_client: GitLabClient):
        self.providers: Dict[BatchDataType, PromptGeneratorStrategyProvider] = {
            BatchDataType.TEST_CODE: TestCodePromptGeneratorStrategyProvider(gitlab_client),
            BatchDataType.PRODUCT: ProductPromptGeneratorStrategyProvider(),
        }

    def get_provider(self, data_type: BatchDataType) -> PromptGenerator:
        if data_type not in self.providers:
            raise ValueError(f"Unsupported data type: {data_type}")
        return self.providers[data_type].provide()
