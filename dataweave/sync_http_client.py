from abc import ABCMeta
from typing import Dict, Any, Optional

from dataweave.proxy_manager import ProxyManager
from sync_session_manager import SyncSessionManager
from http_client import HttpClient


class SyncHttpClient(HttpClient, metaclass=ABCMeta):
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        super().__init__(SyncSessionManager(), proxy_manager=proxy_manager)

    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        return super().request(method, url, headers, **kwargs)