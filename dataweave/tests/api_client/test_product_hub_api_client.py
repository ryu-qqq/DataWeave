import unittest
from unittest.mock import MagicMock
import json

from dataweave.api_client.product_hub_config import ProductHubConfig
from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.sync_http_client import SyncHttpClient

MOCK_RESPONSE = {
    "data": {
        "siteId": 1,
        "siteName": "SETOF",
        "baseUrl": "www.set-of.net",
        "countryCode": "KR",
        "siteType": "CRAWL",
        "siteProfile": {
            "crawlSetting": {
                "crawlFrequency": 10,
                "crawlType": "BEAUTIFUL_SOUP"
            },
            "crawlAuthSetting": {
                "authType": "TOKEN",
                "authEndpoint": "www.set-of.net",
                "authHeaders": "Authorization",
                "authPayload": "Bearer "
            },
            "crawlEndpoints": [
                {
                    "endPointUrl": "/api/v1/product",
                    "crawlTasks": [
                        {
                            "endpointId": 1,
                            "stepOrder": 1,
                            "taskType": "API_CALL",
                            "actionTarget": "",
                            "actionType": "EXTRACT",
                            "params": "",
                            "responseMapping": "{\"product_name\": \"$.name\", \"price\": \"$.price\", \"currency\": \"$.currency\"}"
                        }
                    ]
                }
            ]
        }
    },
    "response": {
        "status": 200,
        "message": "success"
    }
}


class TestProductHubApiClient(unittest.TestCase):
    def setUp(self):
        self.config = ProductHubConfig()
        self.config.BASE_URL = "https://mock-api.com"

        self.http_client = SyncHttpClient()
        self.http_client.request = MagicMock(return_value=json.dumps(MOCK_RESPONSE))

        self.api_client = ProductHubApiClient(config=self.config, http_client=self.http_client)

    def test_fetch_site_context(self):
        result = self.api_client.fetch_site_context(site_id=1)

        # 응답 확인
        self.assertEqual(result.site_id, 1)
        self.assertEqual(result.site_name, "SETOF")
        self.assertEqual(result.base_url, "www.set-of.net")
        self.assertEqual(result.country_code, "KR")
        self.assertEqual(result.site_type, "CRAWL")

        # profile 내 설정 확인
        self.assertEqual(result.site_profile.crawl_setting.crawl_frequency, 10)
        self.assertEqual(result.site_profile.crawl_setting.crawl_type, "BEAUTIFUL_SOUP")
        self.assertEqual(result.site_profile.crawl_auth_setting.auth_type, "TOKEN")
        self.assertEqual(result.site_profile.crawl_auth_setting.auth_endpoint, "www.set-of.net")
        self.assertEqual(result.site_profile.crawl_endpoints[0].end_point_url, "/api/v1/product")

        self.http_client.request.assert_called_once_with(
            "GET",
            "https://mock-api.com/api/v1/site/1",
            headers={"Content-Type": "application/json"}
        )


if __name__ == "__main__":
    unittest.main()
