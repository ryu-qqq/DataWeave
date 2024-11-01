from typing import Dict, Any, Optional

from injector import singleton, inject

from dataweave.proxy_manager import ProxyManager
from dataweave.http_client import HttpClient
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

