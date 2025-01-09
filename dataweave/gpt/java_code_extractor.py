import re

from injector import singleton


@singleton
class JavaCodeExtractor:

    def extract_code(self, raw_data: dict) -> str:
        """
        Extract Java code blocks from a raw_data dictionary.
        """
        try:
            choices = raw_data.get("response", {}).get("body", {}).get("choices", [])
            if not choices:
                raise ValueError("No choices found in response body.")

            code_blocks = []
            for choice in choices:
                message_content = choice.get("message", {}).get("content", "")
                code_block_pattern = r"```java(.*?)```"
                matches = re.finditer(code_block_pattern, message_content, re.DOTALL)
                for match in matches:
                    code_block = match.group(1).strip()
                    if self.__is_valid_java_code(code_block):
                        code_blocks.append(self.__clean_code(code_block))

            if not code_blocks:
                raise ValueError("No valid Java code blocks found.")

            return "\n\n".join(code_blocks)
        except Exception as e:
            raise ValueError(f"Error extracting Java code: {e}")

    def extract_code_from_string(self, raw_data_str: str) -> str:
        """
        Extract Java code blocks from a raw_data string.
        """
        try:
            code_blocks = []
            code_block_pattern = r"```java(.*?)```"
            matches = re.finditer(code_block_pattern, raw_data_str, re.DOTALL)
            for match in matches:
                code_block = match.group(1).strip()
                if self.__is_valid_java_code(code_block):
                    code_blocks.append(self.__clean_code(code_block))

            if not code_blocks:
                raise ValueError("No valid Java code blocks found in string.")

            return "\n\n".join(code_blocks)
        except Exception as e:
            raise ValueError(f"Error extracting Java code from string: {e}")

    def __is_valid_java_code(self, code_block: str) -> bool:
        """
        Validate if the given code block contains valid Java code structure.
        """
        return bool(re.search(r"^(import|public class|class|@|package)", code_block.strip(), re.MULTILINE))

    def __clean_code(self, code_block: str) -> str:
        """
        Clean up the extracted Java code by removing extra whitespaces and blank lines.
        """
        return "\n".join(line.strip() for line in code_block.splitlines() if line.strip())
