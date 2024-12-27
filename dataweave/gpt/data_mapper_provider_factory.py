from injector import singleton, inject
from typing import Dict

from dataweave.enums.source_type import SourceType
from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.data_mapper import DataMapper
from dataweave.gpt.data_mapper_provider import DataMapperProvider, TestCodeDataMapperProvider, ProductDataMapperProvider


@singleton
class DataMapperFactory:

    @inject
    def __init__(self, git_lab_client: GitLabClient):
        self.providers: Dict[SourceType, DataMapperProvider] = {
            SourceType.TEST_CODE: TestCodeDataMapperProvider(git_lab_client),
            SourceType.PRODUCT: ProductDataMapperProvider(),
        }

    def get_mapper(self, source_type: SourceType) -> DataMapper:
        if source_type not in self.providers:
            raise ValueError(f"Unsupported source type: {source_type}")
        return self.providers[source_type].provide()