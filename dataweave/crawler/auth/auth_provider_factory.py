from dataweave.crawler.auth.auth_provider import AuthProvider
from dataweave.crawler.auth.cookie_auth_provider import cookie_auth_provider


class AuthProviderFactory:
    @staticmethod
    def get_auth_provider(auth_type: str) -> AuthProvider:
        if auth_type == "COOKIE":
            return cookie_auth_provider

        raise ValueError(f"Unsupported auth type: {auth_type}")