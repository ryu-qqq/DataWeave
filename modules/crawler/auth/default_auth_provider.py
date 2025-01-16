import json
from typing import Dict

from injector import singleton, inject, Injector

from modules.crawler.auth.auth_interface import AuthInterface


@singleton
class DefaultAuthProvider(AuthInterface):

    @inject
    def __init__(self):
        self.auth_headers = {}

    async def authenticate(self, auth_endpoint: str, headers: Dict[str, str], auth_header: str, payload: str) -> Dict[
        str, str]:
        payload_dict = json.loads(payload)
        headers.update(payload_dict)
        return headers


injector = Injector()
default_auth_provider = injector.get(DefaultAuthProvider)
