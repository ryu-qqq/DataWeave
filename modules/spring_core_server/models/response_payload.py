from typing import Generic, TypeVar, Optional, Dict, Any

T = TypeVar("T")


class Response:
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Response":
        return Response(
            status=data.get("status", 500),
            message=data.get("message", "Unknown error"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
        }


class ApiResponse(Generic[T]):
    def __init__(self, data: Optional[T], response: Response):
        self.data = data
        self.response = response

    @staticmethod
    def from_dict(data: Dict[str, Any], data_type: Optional[type] = None) -> "ApiResponse":
        """
        Converts a dictionary to an ApiResponse object.

        :param data: Dictionary with keys 'data' and 'response'.
        :param data_type: The type of the 'data' field.
        :return: An ApiResponse object.
        """
        response = Response.from_dict(data.get("response", {}))
        if data_type and "data" in data:
            data_content = data_type.from_dict(data["data"]) if data["data"] else None
        else:
            data_content = data.get("data", None)
        return ApiResponse(data=data_content, response=response)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data.to_dict() if hasattr(self.data, "to_dict") else self.data,
            "response": self.response.to_dict(),
        }