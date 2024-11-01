from typing import Any, Optional

class ApiResponse:
    def __init__(self, data: Any, status: int, message: str):
        self.data = data
        self.status = status
        self.message = message

    @staticmethod
    def from_dict(response: dict, data_class: Optional[type] = None) -> 'ApiResponse':
        data = data_class.from_dict(response.get("data", {})) if data_class else response.get("data", {})
        return ApiResponse(
            data=data,
            status=response.get("response", {}).get("status"),
            message=response.get("response", {}).get("message")
        )
