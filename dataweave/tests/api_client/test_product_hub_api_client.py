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
        "siteName": "MUSTIT",
        "baseUrl": "https://m.web.mustit.co.kr",
        "countryCode": "KR",
        "siteType": "CRAWL",
        "siteProfiles": [
            {
                "mappingId": 1,
                "crawlSetting": {
                    "crawlFrequency": 10,
                    "crawlType": "API"
                },
                "crawlAuthSetting": {
                    "authType": "COOKIE",
                    "authEndpoint": "https://m.web.mustit.co.kr",
                    "authHeaders": "Authorization",
                    "authPayload": "\"${token_type} ${token}\""
                },
                "crawlEndpoints": [
                    {
                        "endpointId": 1,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=bino2345&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 1,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 2,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=ccapsule1&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 2,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 3,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=fixedone&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 3,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 4,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=italiagom&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 4,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 5,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=LIKEASTAR&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 5,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 6,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=thefactor2&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 6,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 7,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=viaitalia&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 7,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 8,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=wdrobe&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 8,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    },
                    {
                        "endpointId": 9,
                        "endPointUrl": "/mustit-api/facade-api/v1/search/mini-shop-search",
                        "parameters": "sellerId=BONTANO&pageNo={}&pageSize={}&order=LATEST",
                        "crawlTasks": [
                            {
                                "endpointId": 9,
                                "stepOrder": 1,
                                "taskType": "NONE",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"items\": \"$.items[*]\"}"
                            }
                        ]
                    }
                ],
                "headers": {
                    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                    "Accept": "text/html,application/xhtml+xml",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
                    "Sec-Fetch-User": "?1",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9"
                }
            },
            {
                "mappingId": 2,
                "crawlSetting": {
                    "crawlFrequency": 10,
                    "crawlType": "API"
                },
                "crawlAuthSetting": {
                    "authType": "COOKIE",
                    "authEndpoint": "https://m.web.mustit.co.kr",
                    "authHeaders": "Authorization",
                    "authPayload": "\"${token_type} ${token}\""
                },
                "crawlEndpoints": [
                    {
                        "endpointId": 10,
                        "endPointUrl": "/mustit-api/legacy-api/v1/brands",
                        "parameters": "",
                        "crawlTasks": [
                            {
                                "endpointId": 10,
                                "stepOrder": 1,
                                "taskType": "EXTRACT",
                                "actionTarget": "",
                                "actionType": "SAVE_S3",
                                "params": "{}",
                                "responseMapping": "{\"brands\": \"$.english.*[*].{'brandNo': brandNo, 'brandNameEng': brandNameEng, 'brandNameKor': brandNameKor, 'keyword': keyword}\"}"
                            }
                        ]
                    }
                ],
                "headers": {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,*/*;q=0.8",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Sec-Fetch-Mode": "navigate"
                }
            }
        ]
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
        mock_response = MagicMock()
        mock_response.status_code = 200  # 상태 코드 설정
        mock_response.text = json.dumps(MOCK_RESPONSE_CONTEXT)


        self.http_client.request = MagicMock(return_value=mock_response)
        response = self.api_client.fetch_site_context(site_id=1)
        result = response

        # 응답 확인
        self.assertEqual(result.site_id, 1)
        self.assertEqual(result.site_name, "MUSTIT")
        self.assertEqual(result.base_url, "https://m.web.mustit.co.kr")
        self.assertEqual(result.country_code, "KR")
        self.assertEqual(result.site_type, "CRAWL")

        # profile 내 설정 확인
        self.assertEqual(result.site_profiles[0].crawl_setting.crawl_frequency, 10)
        self.assertEqual(result.site_profiles[0].crawl_setting.crawl_type, "API")
        self.assertEqual(result.site_profiles[0].crawl_auth_setting.auth_type, "COOKIE")
        self.assertEqual(result.site_profiles[0].crawl_auth_setting.auth_endpoint, "https://m.web.mustit.co.kr")
        self.assertEqual(result.site_profiles[0].crawl_endpoints[0].end_point_url, "/mustit-api/facade-api/v1/search/mini-shop-search")
        self.assertEqual(result.site_profiles[0].crawl_endpoints[0].parameters, "sellerId=bino2345&pageNo={}&pageSize={}&order=LATEST")

        self.http_client.request.assert_called_once_with(
            "GET",
            "https://mock-api.com/api/v1/site/1",
            headers={"Content-Type": "application/json"}
        )

    def test_fetch_sites(self):
        mock_response = MagicMock()
        mock_response.status_code = 200  # 상태 코드 설정
        mock_response.text = json.dumps(MOCK_RESPONSE_SITES)  # 텍스트 속성에 JSON 직렬화 데이터 설정

        self.http_client.request = MagicMock(return_value=mock_response)

        # 실제 테스트
        response = self.api_client.fetch_sites(site_type="CRAWL")
        result = response


        # Slice 응답 속성 테스트
        self.assertEqual(result.last, True)
        self.assertEqual(result.first, False)
        self.assertEqual(result.sort, "DESC")
        self.assertEqual(result.size, 20)
        self.assertEqual(result.number_of_elements, 1)
        self.assertEqual(result.empty, False)
        self.assertEqual(result.cursor, 1)
        self.assertEqual(result.total_elements, 1)

        # content 항목 검증
        site = result.content[0]
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
