from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from dataweave.proxy_manager import ProxyManager


class HttpClient(ABC):
    def __init__(self, session_manager, proxy_manager: Optional[ProxyManager] = None):
        self.session = None
        self.session_manager = session_manager
        self.proxy_manager = proxy_manager

    @abstractmethod
    def initialize_session(self):
        """Session을 초기화하는 메서드, 각 하위 클래스에서 구현"""
        pass

    @abstractmethod
    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        """기본 request 메서드로, 다양한 HTTP 메서드를 처리합니다."""
        pass

    @abstractmethod
    def request_response(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        """기본 request 메서드로, 다양한 HTTP 메서드를 처리합니다."""
        pass

    def get(self, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return self.request("GET", url, headers, params=params)

    def post(self, url: str, headers: Dict[str, str], data: Optional[Any] = None) -> Optional[Any]:
        return self.request("POST", url, headers, json=data)

    def put(self, url: str, headers: Dict[str, str], data: Optional[Any] = None) -> Optional[Any]:
        return self.request("PUT", url, headers, json=data)

    def patch(self, url: str, headers: Dict[str, str], data: Optional[Any] = None) -> Optional[Any]:
        return self.request("PATCH", url, headers, json=data)

    def get_response(self, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        return self.request_response("GET", url, headers, params=params)

    def close(self):
        self.session_manager.close_session()

    @abstractmethod
    def _handle_response_errors(self, response, url: str, attempt: int) -> Optional[str]:
        pass
