import json
from typing import List, Dict, Any
from jsonpath_ng import parse

class ApiResponseParser:
    def __init__(self, response_mapping: str):
        self.mapping = json.loads(response_mapping)

    def parse_response(self, response_data: str) -> List[Dict[str, Any]]:
        if not self.mapping:
            return json.loads(response_data)

        response_json = json.loads(response_data)
        extracted_fields = {}

        for key, jsonpath_expression in self.mapping.items():
            jsonpath_expr = parse(jsonpath_expression)
            matches = [match.value for match in jsonpath_expr.find(response_json)]
            extracted_fields[key] = matches

        parsed_data = []
        num_items = len(next(iter(extracted_fields.values())))
        for i in range(num_items):
            entry = {key: extracted_fields[key][i] for key in self.mapping.keys()}
            parsed_data.append(entry)

        return parsed_data
