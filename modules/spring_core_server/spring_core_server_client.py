from typing import Optional, Dict, Any

from injector import singleton, inject

from modules.spring_core_server.spring_core_async_http_client import SpringCoreAsyncHttpClient
from modules.spring_core_server.spring_core_server_config import SpringCoreServerConfig


@singleton
class SpringCoreServerClient:

    @inject
    def __init__(self, config: SpringCoreServerConfig, http_client: SpringCoreAsyncHttpClient):
        self._base_url = config.BASE_URL
        self._http_client = http_client
        self._header = {
            "Content-Type": "application/json",
            "X-AIRFLOW-REQUEST-ID": config.API_KEY,
        }
        print(type(self._http_client))

    async def _make_request(
            self, method: str, endpoint: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None, data: Optional[Any] = None
    ) -> Any:
        """
        Makes an HTTP request and returns the response wrapped in an ApiResponse object.

        :param method: HTTP method (e.g., 'GET').
        :param endpoint: API endpoint relative to the base URL.
        :param headers: Optional HTTP headers.
        :param params: Optional query parameters.
        :return: ApiResponse object.
        :raises ApiResponseException: If an error occurs.
        """
        url = f"{self._base_url}{endpoint}"
        combined_headers = {**self._header, **(headers or {})}

        return await self._http_client.request(method, url, headers=combined_headers, params=params, data=data)
