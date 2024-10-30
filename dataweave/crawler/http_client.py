from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class HttpClient(ABC):
    def __init__(self, session_manager):
        self.session_manager = session_manager

    @abstractmethod
    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    def _handle_response_errors(self, response, url: str, attempt: int) -> Optional[str]:
        pass

    def get(self, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return self.request("GET", url, headers, params=params)

    def post(self, url: str, headers: Dict[str, str], data: Optional[Any] = None) -> Optional[Any]:
        return self.request("POST", url, headers, json=data)

    def put(self, url: str, headers: Dict[str, str], data: Optional[Any] = None) -> Optional[Any]:
        return self.request("PUT", url, headers, json=data)

    def patch(self, url: str, headers: Dict[str, str], data: Optional[Any] = None) -> Optional[Any]:
        return self.request("PATCH", url, headers, json=data)

    def close(self):
        self.session_manager.close_session()