import json
import logging
from typing import List

from dataweave.enums.product_data_type import BatchDataType
from dataweave.gpt.batch_product_models import BatchProductModel
from dataweave.gpt.batch_product_models_provider import BatchProductProvider


def sanitize_json_string(json_string: str) -> str:
    """
    JSON 문자열을 정리하여 유효하지 않은 제어 문자를 제거합니다.
    """
    try:
        json_string = json_string.replace("\\n", " ").replace("\\r", " ").replace("\\t", " ")
        json_string = json_string.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        return json_string
    except Exception as e:
        logging.error(f"Error sanitizing JSON string: {e}")
        raise ValueError(f"Invalid JSON string: {json_string}")


class BatchDataMapper:

    @staticmethod
    def extract_content(data_type: BatchDataType, file_path: str) -> List[BatchProductModel]:
        try:
            response_contents = []
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        response = item.get("response", {}).get("body", {}).get("choices", [])
                        for choice in response:
                            content = choice.get("message", {}).get("content")
                            if content:
                                content_cleaned = sanitize_json_string(content.strip("```json").strip("```").strip())
                                parsed_content = json.loads(content_cleaned)

                                response_contents.append(BatchProductProvider.from_json(data_type, parsed_content))

                    except json.JSONDecodeError as e:
                        logging.error(f"Invalid JSON line: {line}")
                        raise ValueError(f"Error decoding JSON in line: {line}. Error: {e}")
            return response_contents
        except Exception as e:
            raise ValueError(f"Error processing batch file {file_path}: {e}")
