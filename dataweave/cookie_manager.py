import logging
from typing import Dict, Any
from injector import singleton, inject
from http_client import HttpClient


@singleton
class CookieManager:
    @inject
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    async def get_cookies(self, url: str, headers: Dict[str, str], session=None) -> Dict[str, Any]:
        response = await self.http_client.get(url, headers, {})
        if response:
            cookies = {}
            for cookie in response.cookies.values():
                cookie_details = {
                    "value": cookie.value,
                    "domain": cookie['domain'],
                    "path": cookie['path'],
                    "expires": cookie.get('expires'),
                    "max-age": cookie.get('max-age'),
                    "secure": cookie['secure'],
                    "httponly": cookie.get('httponly', False),
                    "samesite": cookie.get('samesite')
                }
                cookies[cookie.key] = cookie_details
            return cookies
        else:
            logging.error(
                f"Failed to retrieve cookies from {url}, status: {response.status if response else 'No response'}")
            return {}
