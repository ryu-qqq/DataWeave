import asyncio
import json
from abc import abstractmethod, ABC
from typing import Any, List

from injector import singleton

from dataweave.api_client.models.git_event_context_response import GitEventContextResponse
from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse
from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.models.product_data import ProductData
from dataweave.gpt.models.test_code_data import TestCodeData, PublicMethodDomain, CodeClassDomain


class DataMapper(ABC):
    @abstractmethod
    def map(self, external_data: Any) -> Any:
        pass


@singleton
class TestCodeDataMapper(DataMapper):
    def __init__(self, gitlab_client: GitLabClient):
        self.gitlab_client = gitlab_client

    async def map(self, external_data: GitEventContextResponse) -> List[TestCodeData]:
        git_event = external_data.git_event

        filtered_files = [
            file for file in external_data.change_files
            if file.code_class and file.code_class.requires_test
        ]

        await asyncio.gather(
            *(file.load_content(
                gitlab_client=self.gitlab_client,
                project_id=git_event.project_id,
                branch_name=git_event.branch_name
            ) for file in filtered_files)
        )

        test_code_data_list = []

        for changed_file in filtered_files:
            code_class = changed_file.code_class

            public_methods = [
                PublicMethodDomain(
                    method_name=method.method_name,
                    return_type=method.return_type,
                    parameters=json.loads(method.parameter),
                    return_type_fields=json.loads(method.return_type_fields)
                )
                for method in code_class.public_methods
            ]

            code_class_domain = CodeClassDomain(
                class_name=code_class.class_name,
                requires_test=code_class.requires_test,
                test_generate=code_class.test_generate,
                public_methods=public_methods
            )

            test_code_data_list.append(
                TestCodeData(
                    branch_name=git_event.branch_name,
                    project_id=git_event.project_id,
                    commit_id=git_event.commit_id,
                    commit_message=git_event.commit_message,
                    repository_name=git_event.repository_name,
                    status=git_event.status,
                    error_message=git_event.error_message,
                    file_path=changed_file.file_path,
                    change_type=changed_file.change_type,
                    code_class=code_class_domain,
                    file_content=changed_file.file_content
                )
            )

        return test_code_data_list


@singleton
class ProductDataMapper(DataMapper):
    def map(self, external_data: GptTrainingDataResponse) -> ProductData:
        return ProductData(
            product_group_id=external_data.product_group.product_group_id,
            product_group_name=external_data.product_group.product_group_name,
            brand_name=external_data.brand.brand_name,
            categories=[category.category_name for category in external_data.categories],
            products=[product.option for product in external_data.products]
        )
