from datetime import datetime, timedelta
from typing import Dict, Optional


class CrawlAuthContext:
    def __init__(self, auth_type: str, auth_endpoint: str, headers: Dict[str, str], auth_payload: Optional[str] = None):
        self.auth_type = auth_type
        self.auth_endpoint = auth_endpoint
        self.headers = headers
        self.auth_payload = auth_payload
        self.auth_token = None
        self.expiration_time = None

    def update_headers(self, new_headers: Dict[str, str], ttl: int):
        self.headers.update(new_headers)
        self.expiration_time = datetime.now() + timedelta(seconds=ttl)

    def is_valid(self) -> bool:
        return self.expiration_time and datetime.now() < self.expiration_time


