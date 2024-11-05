from typing import Dict, Any


class CustomResponseParser:
    def parse_response(self, response_data: str) -> Dict[str, Any]:
        raise NotImplementedError("Custom parsers must implement `parse_response` method")