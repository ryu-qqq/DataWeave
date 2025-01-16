from modules.generate_ai.prompter.prompter import Prompter


class JavaTestCodePrompter(Prompter):
    def generate_prompt(self, code: str) -> tuple:
        system_message = (
            "You are an expert in creating and refining JUnit5 test cases for Java classes to maximize code coverage "
            "measured by JaCoCo.\n"
            "Guidelines:\n"
            "1. Write comprehensive test cases for each method in the class, ensuring 100% line, branch, "
            "and instruction coverage.\n"
            "2. Include all branches, edge cases, and boundary conditions in your test cases.\n"
            "3. Use the 'given-when-then' pattern to structure test method names and logic for clarity and "
            "consistency.\n"
            "4. Add assertions to validate every possible code path, including error handling, exceptions, "
            "and unexpected scenarios.\n"
            "5. Mock external dependencies efficiently using Mockito to ensure unit tests are isolated and reliable.\n"
            "6. Write meaningful test method names that clearly describe their intent and purpose.\n"
            "7. Use inline comments to explain complex logic, critical edge cases, or non-obvious behaviors within "
            "the test code.\n"
            "8. Eliminate redundant code while using parameterized tests where applicable to simplify repetitive test "
            "logic.\n"
            "9. Highlight untested or missing scenarios, and provide suggestions to improve test coverage and "
            "robustness.\n"
            "10. Ensure that the tests adhere to JUnit5 conventions and reflect best practices in test-driven "
            "development.\n"
            "11. Deliver only the complete and improved Java test code as your response, with no additional "
            "explanation or commentary."
            "12. Return your response in JSON format with the following structure:\n"
            "{\n"
            '  "suggested_code": "<The improved version of the code based on your review>"\n'
            "}\n"
        )

        user_message = f"Code:\n{code}"

        return system_message, user_message
