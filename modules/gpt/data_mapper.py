import asyncio
from abc import abstractmethod, ABC
from typing import Any, List

from injector import singleton

from modules.git_lab.git_lab_client import GitLabClient
from dataweave.api_client.models.git_event_context_response import GitEventContextResponse
from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse
from modules.gpt.models.product_data import ProductData
from modules.gpt.models.test_code_data_models import TestCodeData


class DataMapper(ABC):
    @abstractmethod
    def map(self, external_data: Any) -> Any:
        pass


@singleton
class TestCodeDataMapper(DataMapper):
    def __init__(self, gitlab_client: GitLabClient):
        self.gitlab_client = gitlab_client

    async def map(self, external_data: List[GitEventContextResponse]) -> List[TestCodeData]:
        test_code_data_list = []
        for git_event_response in external_data:
            git_event = git_event_response.git_event

            filtered_files = [
                file for file in git_event_response.change_files
                if file.file_content
            ]

            await asyncio.gather(
                *(file.load_content(
                    gitlab_client=self.gitlab_client,
                    project_id=git_event.project_id,
                    branch_name=git_event.branch_name
                ) for file in filtered_files)
            )

            for changed_file in filtered_files:

                original_file_path = changed_file.file_path
                test_file_path = self.__generate_test_file_path(original_file_path)

                test_code_data_list.append(
                    TestCodeData(
                        id=git_event.id,
                        branch_name=git_event.branch_name,
                        project_id=git_event.project_id,
                        commit_id=changed_file.commit_id,
                        commit_message=changed_file.commit_message,
                        repository_name=git_event.repository_name,
                        status=git_event.status,
                        file_path=test_file_path,
                        change_type=changed_file.change_type,
                        file_content=changed_file.file_content
                    )
                )

        return test_code_data_list

    @staticmethod
    def __generate_test_file_path(original_file_path: str) -> str:
        if "src/main/java" not in original_file_path:
            raise ValueError(f"Invalid file path: {original_file_path}")

        test_path = original_file_path.replace("src/main/java", "src/test/java")

        if test_path.endswith(".java"):
            base_name = test_path[:-5]
            test_path = f"{base_name}Test.java"

        return test_path

@singleton
class ProductDataMapper(DataMapper):

    def map(self, external_data: List[GptTrainingDataResponse]) -> List[ProductData]:
        mapped_data = []
        for item in external_data:
            mapped_data.append(ProductData(
                id=item.product_group.product_group_id,
                product_group_name=item.product_group.product_group_name,
                brand_name=item.brand.brand_name,
                categories=[category.category_name for category in item.categories],
                products=[product.option for product in item.products]
            ))
        return mapped_data


