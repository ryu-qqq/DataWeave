from typing import Any

from modules.spring_core_server.models.response_payload import ApiResponse


class ApiResponseHandler:
    @staticmethod
    def handle_response(api_response: ApiResponse) -> Any:
        """
        Handles the API response. Extracts and returns the data if the status is 200.

        :param api_response: ApiResponse object.
        :return: Extracted data if the response is successful; raises an exception otherwise.
        """
        if api_response.response.status == 200:
            return api_response.data
        else:
            raise ValueError(
                f"API responded with error: {api_response.response.status} - {api_response.response.message}"
            )
