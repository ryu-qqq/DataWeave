import json
import tempfile
from typing import List

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from injector import singleton, inject

from dataweave.antlr import JavaLexer
from dataweave.antlr import JavaParser
from dataweave.cache.test_code_cache_manager import TestCodeCacheManager
from dataweave.gitlab.git_lab_client import GitLabClient
from dataweave.gpt.method_extractor import MethodExtractor
from dataweave.gpt.models.test_code_data import TestCodeData
from dataweave.gpt.prompt import Prompt
from dataweave.gpt.prompt_generator import PromptGenerator


@singleton
class TestCodePromptGenerator(PromptGenerator):

    @inject
    def __init__(self, gitlab_client: GitLabClient, test_code_cache_manager: TestCodeCacheManager):
        self.gitlab_client = gitlab_client
        self.test_code_cache_manager = test_code_cache_manager

    async def get_prompt(self, test_code_data: TestCodeData) -> List[Prompt]:
        await test_code_data.load_file_content(self.gitlab_client)

        await self.test_code_cache_manager.initialize_commit(
            commit_id=test_code_data.commit_id,
            class_name=test_code_data.code_class.class_name,
            methods=[method.method_name for method in test_code_data.code_class.public_methods]
        )

        system_message = (
            "You are an expert in generating unit tests for Java. "
            "Focus on generating accurate test cases for the given method. "
            "Use mocking frameworks (e.g., Mockito) where applicable. "
            "Return only the test code in the following format: \n\n"
            "```java\n<test_code>\n```\n"
        )

        prompts = []
        for method in test_code_data.code_class.public_methods:
            method_code = self.extract_method_content_with_antlr(
                file_content=test_code_data.file_content,
                method_name=method.method_name
            )

            user_message = (
                f"Method Name: {method.method_name}\n"
                f"Parameters: {json.dumps(method.parameters)}\n\n"
                f"Return Type: {method.return_type}\n"
                f"Return Type Fields: {json.dumps(method.return_type_fields)}\n\n"
                f"Method Code:\n{method_code}"
            )

            metadata = {
                "commit_id": test_code_data.commit_id,
                "file_path": test_code_data.file_path,
                "project_id": test_code_data.project_id,
                "branch_name": test_code_data.branch_name,
                "commit_message": test_code_data.commit_message,
                "method_name": method.method_name,
            }

            prompts.append(Prompt(system_message, user_message, metadata))

        return prompts

    def extract_method_content_with_antlr(self, file_content, method_name):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as temp_file:
                temp_file.write(file_content.encode('utf-8'))
                temp_file_path = temp_file.name

            lexer = JavaLexer(FileStream(temp_file_path))
            stream = CommonTokenStream(lexer)
            parser = JavaParser(stream)
            tree = parser.compilationUnit()

            extractor = MethodExtractor(method_name, stream)
            walker = ParseTreeWalker()
            walker.walk(extractor, tree)

            return extractor.method_content or f"Method {method_name} not found."
        except Exception as e:
            return f"Error while extracting method {method_name}: {str(e)}"
