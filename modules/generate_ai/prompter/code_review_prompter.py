from modules.generate_ai.prompter.prompter import Prompter


class JavaCodeReviewPrompter(Prompter):
    def generate_prompt(self, code: str) -> tuple:

        system_message = (
            "You are Robert C. Martin, a renowned expert in clean code principles. "
            "Review the following Java code and provide feedback on how to improve its structure, readability, "
            "and maintainability while adhering to clean code practices.\n\n"
            "Additionally, determine whether this code requires unit tests. "
            "If tests are required, include 'test_required': true in your response. "
            "Otherwise, set it to false.\n\n"
            "Return your response in JSON format with the following structure:\n"
            "{\n"
            '  "review": "<Your detailed review of the original code>",\n'
            '  "suggested_code": "<The improved version of the code based on your review>",\n'
            '  "test_required": <true or false>\n'
            "}\n\n"
            f"Code:\n{code}"
        )

        user_message = f"Code:\n{code}"

        return system_message, user_message
