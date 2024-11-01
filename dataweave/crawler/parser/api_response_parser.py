import json

from typing import Dict, Any
from jsonpath_ng import parse


class ApiResponseParser:
    def __init__(self, response_mapping: str):
        self.mapping = json.loads(response_mapping)

    def parse_response(self, response_data: str) -> Dict[str, Any]:
        response_json = json.loads(response_data)
        parsed_data = {}

        for key, jsonpath_expression in self.mapping.items():
            jsonpath_expr = parse(jsonpath_expression)
            match = [match.value for match in jsonpath_expr.find(response_json)]
            parsed_data[key] = match if len(match) > 1 else (match[0] if match else None)

        return parsed_data
