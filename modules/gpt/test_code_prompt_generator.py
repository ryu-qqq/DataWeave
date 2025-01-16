from typing import List

from injector import singleton, inject

from modules.git_lab.git_lab_client import GitLabClient
from modules.antlr.java_method_extractor import JavaMethodExtractor
from modules.gpt.models.test_code_data_models import TestCodeData
from modules.gpt.models.prompt_models import Prompt, TestCodeMetadata
from modules.gpt.prompt_generator import PromptGenerator


@singleton
class TestCodePromptGenerator(PromptGenerator):

    @inject
    def __init__(self,
                 gitlab_client: GitLabClient,
                 ):
        self.gitlab_client = gitlab_client

    async def get_prompt(self, test_code_data: TestCodeData) -> List[Prompt]:
        await test_code_data.load_file_content(self.gitlab_client)

        system_message = (
            "You are an expert in generating JUnit5 test cases for Java classes.\n"
            "Follow these guidelines for each test case:\n"
            "1. Use @DisplayName for every test to describe its purpose.\n"
            "2. Follow the 'given-when-then' pattern for test method names.\n"
            "3. Include typical use cases, edge cases, and boundary values.\n"
            "4. Mock external dependencies using Mockito.\n"
            "5. Ensure all generated tests are well-structured and self-contained.\n"
            "6. If any imported class is missing, assume it exists in the same package as this class.\n"

        )

        extractor = JavaMethodExtractor()
        methods = extractor.extract_method(test_code_data.file_content)


        method_details = ""
        for method in methods:
            method_details += (
                f"\n- Method Name: {method.method_name}\n"
                f"  Return Type: {method.return_type}\n"
                f"  Parameters: {method.parameters}\n"
                f"  Return Value Fields: {method.return_type_fields}\n"
            )

        user_message = (
            f"Class Name: {test_code_data.code_class.class_name}\n"
            f"File Path: {test_code_data.file_path}\n\n"
            f"Full Code:\n{test_code_data.file_content}\n\n"
            f"Public Methods Details:{method_details}\n\n"
            "Please generate JUnit5 test cases for each method in this class. "
            "Include edge cases, boundary conditions, and error handling scenarios."
        )

        metadata = TestCodeMetadata(
            id=test_code_data.id,
            commit_id=test_code_data.commit_id,
            class_name=test_code_data.code_class.class_name,
            project_id=test_code_data.project_id,
            branch_name=test_code_data.branch_name,
            file_path=test_code_data.file_path,
            commit_message=test_code_data.commit_message,
        )

        return [Prompt[TestCodeMetadata](system_message, user_message, metadata)]
