from typing import Dict

from injector import singleton, inject

from modules.git_lab.git_lab_client import GitLabClient
from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.data_mapper import DataMapper
from modules.gpt.data_mapper_provider import DataMapperProvider, TestCodeDataMapperProvider, \
    ProductDataMapperProvider


@singleton
class DataMapperFactory:

    @inject
    def __init__(self, git_lab_client: GitLabClient):
        self.providers: Dict[BatchDataType, DataMapperProvider] = {
            BatchDataType.TEST_CODE: TestCodeDataMapperProvider(git_lab_client),
            BatchDataType.PRODUCT: ProductDataMapperProvider(),
        }

    def get_mapper(self, batch_data_type: BatchDataType) -> DataMapper:
        if batch_data_type not in self.providers:
            raise ValueError(f"Unsupported batch data type: {batch_data_type}")
        return self.providers[batch_data_type].provide()