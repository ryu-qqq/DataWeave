import re

from typing import Dict, Any
from string import Template
from injector import inject, singleton, Injector
from modules.http_client.cookie_manager import CookieManager
from modules.crawler.auth.auth_interface import AuthInterface


@singleton
class CookieAuthProvider(AuthInterface):

    @inject
    def __init__(self, cookie_manager: CookieManager):
        self.cookie_manager = cookie_manager
        self.auth_headers = {}

    async def authenticate(self, auth_endpoint: str, headers: Dict[str, str], auth_header: str, payload: str) -> \
            (Dict[str, str], int):
        cookies = await self.cookie_manager.get_cookies(auth_endpoint, headers)
        if not cookies:
            raise ValueError("Failed to retrieve cookies for authentication.")

        auth_headers = self.set_dynamic_headers(auth_header, cookies, payload)

        headers.update(auth_headers)
        ttl = 3600
        return headers, ttl

    @staticmethod
    def set_dynamic_headers(auth_header: str, cookies: Dict[str, Any], payload: str) -> Dict[str, str]:
        template = Template(payload)
        required_keys = re.findall(r'\$\{(.*?)\}', payload)

        context = {key: cookies.get(key, {}).get('value', '') for key in required_keys}

        substituted_text = template.safe_substitute(**context).strip()
        clean_text = substituted_text.replace('"', '')

        return {auth_header: clean_text}


injector = Injector()
cookie_auth_provider = injector.get(CookieAuthProvider)
