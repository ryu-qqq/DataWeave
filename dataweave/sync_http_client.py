import logging
from typing import Dict, Any, Optional

from injector import singleton

from dataweave.client_exception import UnauthorizedException, ForbiddenException, TooManyRequestException, \
    UnExpectedException
from dataweave.http_client import HttpClient
from dataweave.proxy_manager import ProxyManager
from dataweave.sync_session_manager import SyncSessionManager


@singleton
class SyncHttpClient(HttpClient):

    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        super().__init__(SyncSessionManager(), proxy_manager=proxy_manager)

    def initialize_session(self):
        self.session = self.session_manager.create_session()

    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        if not self.session:
            self.initialize_session()
        proxies = {"http": self.proxy_manager.get_proxy()} if self.proxy_manager else None
        response = self.session.request(method, url, headers=headers, proxies=proxies, **kwargs)
        return response.text if response.status_code == 200 else self._handle_response_errors(response, url, 0)

    def request_response(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        if not self.session:
            self.initialize_session()
        proxies = {"http": self.proxy_manager.get_proxy()} if self.proxy_manager else None
        response = self.session.request(method, url, headers=headers, proxies=proxies, **kwargs)
        return response if response.status_code == 200 else self._handle_response_errors(response, url, 0)

    def _handle_response_errors(self, response, url: str, attempt: int) -> Optional[str]:
        text = response.text
        status = response.status_code

        if status == 401:
            logging.error(f"Unauthorized (401) error for {url}. Check your credentials.")
            raise UnauthorizedException("Token expired, fetching new token.")
        elif status == 403:
            logging.error(f"Forbidden (403) error for {url}. Check your permissions.")
            raise ForbiddenException("Token expired, fetching new token.")
        elif status == 429:
            logging.error(f"Too Many Requests (429). Retrying {url} after backoff.")
            raise TooManyRequestException("Too Many Requests (429)")
        elif status == 200:
            return text
        else:
            logging.error(f"Received status {status} from {url}: {text}")
            raise UnExpectedException("UnExpected Error")
