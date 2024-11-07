import json

from typing import Dict, Any, List
from jsonpath_ng import parse


class ApiResponseParser:
    def __init__(self, response_mapping: str):
        self.mapping = json.loads(response_mapping)

    def parse_response(self, response_data: str) -> List[Dict[str, Any]]:
        response_json = json.loads(response_data)
        extracted_fields = {}

        # 각 필드에 대해 JSONPath로 값을 추출
        for key, jsonpath_expression in self.mapping.items():
            jsonpath_expr = parse(jsonpath_expression)
            matches = [match.value for match in jsonpath_expr.find(response_json)]
            extracted_fields[key] = matches

        # 필드 값들을 동적으로 매핑하여 각 항목을 구성
        parsed_data = []
        num_items = len(next(iter(extracted_fields.values())))  # 첫 필드의 항목 수를 기준으로 설정
        for i in range(num_items):
            entry = {key: extracted_fields[key][i] for key in self.mapping.keys()}
            parsed_data.append(entry)

        return parsed_data
