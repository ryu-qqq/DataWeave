from typing import Any, Optional, Type


class ApiResponse:
    def __init__(self, data: Any, status: int, message: str):
        self.data = data
        self.status = status
        self.message = message

    @staticmethod
    def from_dict(response: dict, data_class: Optional[Type] = None) -> 'ApiResponse':
        data = response.get("data", [])
        if data_class and isinstance(data, list):
            data = [data_class.from_dict(item) for item in data]
        elif data_class:
            data = data_class.from_dict(data)
        return ApiResponse(
            data=data,
            status=response.get("response", {}).get("status"),
            message=response.get("response", {}).get("message")
        )
