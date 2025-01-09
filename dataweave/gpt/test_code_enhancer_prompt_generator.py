from injector import singleton, inject

from dataweave.gpt.java_code_extractor import JavaCodeExtractor
from dataweave.gpt.models.prompt_models import Prompt


@singleton
class TestCodeEnhancerPromptGenerator:

    @inject
    def __init__(self, java_code_extractor: JavaCodeExtractor):
        self.__java_code_extractor = java_code_extractor

    def get_prompt(self, raw_data: dict) -> Prompt:
        try:
            java_code = self.__java_code_extractor.extract_code(raw_data)

            system_message = (
                "You are an expert in creating and refining JUnit5 test cases for Java classes to maximize code coverage measured by JaCoCo.\n"
                "Guidelines:\n"
                "1. Ensure each method in the class has comprehensive test cases, including all branches, edge cases, and boundary conditions.\n"
                "2. Follow the 'given-when-then' pattern for test method names and structure.\n"
                "3. Add assertions to validate all possible code paths, including error handling and unexpected scenarios.\n"
                "4. Mock external dependencies efficiently using Mockito, and ensure tests are isolated.\n"
                "5. Use meaningful names for test methods that clearly describe their intent.\n"
                "6. Add inline comments to clarify complex logic or important edge cases.\n"
                "7. Eliminate redundancy while ensuring 100% line, branch, and instruction coverage as measured by JaCoCo.\n"
                "8. Use parameterized tests where applicable to avoid repetitive code.\n"
                "9. Highlight missing or untested scenarios and suggest improvements.\n"
                "10. Ensure tests adhere to best practices and follow JUnit5 conventions.\n"
                "11. Provide only the complete and improved Java test code without any additional explanation or context.\n"
            )

            user_message = (
                f"Here is the existing test code for improvement:\n\n{java_code}\n\n"
                "Please review and optimize the above test cases based on the guidelines to maximize JaCoCo coverage. "
                "Highlight any missing scenarios and ensure the tests are efficient, isolated, and comprehensive."
            )

            return Prompt(system_message=system_message, user_message=user_message, metadata=None)
        except Exception as e:
            raise ValueError(f"Error generating prompt: {e}")
