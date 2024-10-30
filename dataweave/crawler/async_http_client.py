from typing import Dict, Any, Optional


class SyncHttpClient(HttpClient):
    def __init__(self):
        super().__init__(SyncSessionManager())

    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        session = self.session_manager.create_session()
        response = session.request(method, url, headers=headers, **kwargs)
        return response.text if response.status_code == 200 else self._handle_response_errors(response, url, 0)


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
