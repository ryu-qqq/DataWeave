from dataweave.crawler.auth.auth_interface import AuthInterface
from dataweave.crawler.auth.cookie_auth_provider import cookie_auth_provider
from dataweave.enums.auth_type import AuthType


class AuthProvider:
    @staticmethod
    def get_auth_provider(auth_type: str) -> AuthInterface:
        if auth_type == AuthType.COOKIE.name:
            return cookie_auth_provider

        raise ValueError(f"Unsupported auth type: {auth_type}")