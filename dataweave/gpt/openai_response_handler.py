from injector import singleton, inject

from dataweave.gpt.java_code_extractor import JavaCodeExtractor


@singleton
class OpenAIResponseHandler:

    @inject
    def __init__(self, java_code_extractor: JavaCodeExtractor):
        self.__java_code_extractor = java_code_extractor

    def extract_enhanced_code(self, response: dict) -> str:
        try:
            return self.__java_code_extractor.extract_code(response)
        except Exception as e:
            raise ValueError(f"Error extracting enhanced code: {e}")


    def extract_enhanced_code_from_string(self, response: str) -> str:
        try:
            return self.__java_code_extractor.extract_code_from_string(response)
        except Exception as e:
            raise ValueError(f"Error extracting enhanced code: {e}")
