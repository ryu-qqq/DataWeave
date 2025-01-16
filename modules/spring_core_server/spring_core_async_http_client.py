import json
import logging
from typing import Optional, Dict, Any

from injector import singleton

from dataweave.api_client.models.product_hub_api_response import ApiResponse
from modules.http_client.async_http_client import AsyncHttpClient


@singleton
class SpringCoreAsyncHttpClient(AsyncHttpClient):

    """
    Spring Core Server-specific Async HTTP Client.
    Automatically processes responses in the ApiResponse format.
    """
    async def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Optional[Any]:
        """
        Sends an HTTP request and returns the `data` field of the ApiResponse.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param url: Full endpoint URL.
        :param headers: HTTP headers.
        :return: Parsed `data` field of the ApiResponse.
        """
        response_text = await super().request(method, url, headers=headers, **kwargs)
        try:
            response_json = json.loads(response_text)
            api_response = ApiResponse.from_dict(response_json)
            return self._handle_api_response(api_response)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")
            raise ValueError(f"Invalid JSON response from {url}")
        except Exception as e:
            logging.error(f"Unexpected error while handling response from {url}: {e}")
            raise

    async def request_response(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> ApiResponse:
        """
        Sends an HTTP request and returns the full ApiResponse object.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param url: Full endpoint URL.
        :param headers: HTTP headers.
        :return: ApiResponse object containing `data` and `response`.
        """
        response_text = await super().request(method, url, headers=headers, **kwargs)
        try:
            response_json = json.loads(response_text)
            return ApiResponse.from_dict(response_json)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response from {url}: {e}")
            raise ValueError(f"Invalid JSON response from {url}")

    def _handle_api_response(self, api_response: ApiResponse) -> Any:
        """
        Extracts the `data` field from an ApiResponse or raises an error if the status is not 200.

        :param api_response: ApiResponse object.
        :return: Extracted `data` field.
        """
        if api_response.response.status == 200:
            return api_response.data
        else:
            logging.error(
                f"Spring Core Server API Error: {api_response.response.status} - {api_response.response.message}"
            )
            raise ValueError(
                f"API responded with error: {api_response.response.status} - {api_response.response.message}"
            )
