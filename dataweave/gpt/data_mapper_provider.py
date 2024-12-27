from abc import ABC, abstractmethod

from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.data_mapper import DataMapper, TestCodeDataMapper, ProductDataMapper


class DataMapperProvider(ABC):
    @abstractmethod
    def provide(self) -> DataMapper:
        pass


class TestCodeDataMapperProvider(DataMapperProvider):
    def __init__(self, git_lab_client: GitLabClient):
        self.git_lab_client = git_lab_client

    def provide(self) -> DataMapper:
        return TestCodeDataMapper(self.git_lab_client)


class ProductDataMapperProvider(DataMapperProvider):
    def provide(self) -> DataMapper:
        return ProductDataMapper()
