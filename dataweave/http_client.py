from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from client_exception import *
from proxy_manager import ProxyManager


class HttpClient(ABC):
    def __init__(self, session_manager, proxy_manager: Optional[ProxyManager] = None):
        self.session_manager = session_manager
        self.proxy_manager = proxy_manager

    @abstractmethod
    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        """기본 request 메서드로, 다양한 HTTP 메서드를 처리합니다."""
        session = self.session_manager.create_session()
        proxies = {"http": self.proxy_manager.get_proxy()} if self.proxy_manager else None
        response = session.request(method, url, headers=headers, proxies=proxies, **kwargs)
        return response.text if response.status_code == 200 else self._handle_response_errors(response, url, 0)

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

    @abstractmethod
    def _handle_response_errors(self, response, url: str, attempt: int) -> Optional[str]:
        text = response.text
        status = response.status_code

        if status == 401:
            print(f"Unauthorized (401) error for {url}. Check your credentials.")
            raise UnauthorizedException("Token expired, fetching new token.")
        elif status == 403:
            print(f"Forbidden (403) error for {url}. Check your permissions.")
            raise ForbiddenException("Token expired, fetching new token.")
        elif status == 429:
            print(f"Too Many Requests (429). Retrying {url} after backoff.")
            import time
            time.sleep(min((2 ** attempt) * 60, 300))
        else:
            print(f"Received status {status} from {url}: {text}")
        return None