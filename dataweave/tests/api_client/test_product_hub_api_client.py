import unittest
from unittest.mock import MagicMock
import json

from dataweave.api_client.models.site_response import SiteResponse
from dataweave.api_client.models.slice import Slice
from dataweave.api_client.product_hub_config import ProductHubConfig
from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.sync_http_client import SyncHttpClient

MOCK_RESPONSE_CONTEXT = {
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
                    "parameters": "sellerId=LIKEASTAR&pageNo={}&pageSize={}&order=LATEST",
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

MOCK_RESPONSE_SITES = {
    "data": {
        "content": [
            {
                "siteId": 1,
                "siteName": "MUSTIT",
                "baseUrl": "https://m.web.mustit.co.kr",
                "countryCode": "KR",
                "siteType": "CRAWL"
            }
        ],
        "last": True,
        "first": False,
        "sort": "DESC",
        "size": 20,
        "numberOfElements": 1,
        "empty": False,
        "cursor": 1,
        "totalElements": 1
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
        self.api_client = ProductHubApiClient(config=self.config, http_client=self.http_client)

    def test_fetch_site_context(self):
        self.http_client.request = MagicMock(return_value=json.dumps(MOCK_RESPONSE_CONTEXT))
        result = self.api_client.fetch_site_context(site_id=1)

        # 응답 확인
        self.assertEqual(result.site_id, 1)
        self.assertEqual(result.site_name, "SETOF")
        self.assertEqual(result.base_url, "www.set-of.net")
        self.assertEqual(result.country_code, "KR")
        self.assertEqual(result.site_type, "CRAWL")

        # profile 내 설정 확인
        self.assertEqual(result.site_profiles[0].crawl_setting.crawl_frequency, 10)
        self.assertEqual(result.site_profiles[0].crawl_setting.crawl_type, "BEAUTIFUL_SOUP")
        self.assertEqual(result.site_profiles[0].crawl_auth_setting.auth_type, "TOKEN")
        self.assertEqual(result.site_profiles[0].crawl_auth_setting.auth_endpoint, "www.set-of.net")
        self.assertEqual(result.site_profiles[0].crawl_endpoints[0].end_point_url, "/api/v1/product")
        self.assertEqual(result.site_profiles[0].crawl_endpoints[0].parameters, "sellerId=LIKEASTAR&pageNo={}&pageSize={}&order=LATEST")

        self.http_client.request.assert_called_once_with(
            "GET",
            "https://mock-api.com/api/v1/site/1",
            headers={"Content-Type": "application/json"}
        )

    def test_fetch_sites(self):
        self.http_client.request = MagicMock(return_value=json.dumps(MOCK_RESPONSE_SITES))
        response_data = self.api_client.fetch_sites(site_type="CRAWL")

        # Slice 응답 속성 테스트
        self.assertEqual(response_data.last, True)
        self.assertEqual(response_data.first, False)
        self.assertEqual(response_data.sort, "DESC")
        self.assertEqual(response_data.size, 20)
        self.assertEqual(response_data.number_of_elements, 1)
        self.assertEqual(response_data.empty, False)
        self.assertEqual(response_data.cursor, 1)
        self.assertEqual(response_data.total_elements, 1)

        # content 항목 검증
        site = response_data.content[0]
        self.assertEqual(site.site_id, 1)
        self.assertEqual(site.site_name, "MUSTIT")
        self.assertEqual(site.base_url, "https://m.web.mustit.co.kr")
        self.assertEqual(site.country_code, "KR")
        self.assertEqual(site.site_type, "CRAWL")

        # 요청 확인
        self.http_client.request.assert_called_once_with(
            "GET",
            "https://mock-api.com/api/v1/site",
            headers={"Content-Type": "application/json"},
            params={"siteType": "CRAWL", "cursorId": None, "pageSize": 20}
        )


if __name__ == "__main__":
    unittest.main()
