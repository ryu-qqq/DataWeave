import asyncio
import json

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.task.crawl_task_executor import CrawlTaskExecutor, crawl_task_executor

if __name__ == "__main__":
    json_data = """
       {
           "mappingId": 15,
           "crawlSetting": {
               "crawlFrequency": 10,
               "crawlType": "API"
           },
           "crawlAuthSetting": {
               "authType": "COOKIE",
               "authEndpoint": "https://m.web.mustit.co.kr",
               "authHeaders": "Authorization",
               "authPayload": "${token_type} ${token}"
           },
           "crawlEndpoints": [
               {
                   "endpointId": 21,
                   "endPointUrl": "/mustit-api",
                   "parameters": "",
                   "crawlTasks": [
                       {
                                "endpointId": 21,
                                "stepOrder": 2,
                                "type": "CRAWLING",
                                "target": "PRODUCT",
                                "action": "SAVE_S3",
                                "params": {"siteProductId": "${crawl_product_sku}"},
                                "endPointUrl": "/facade-api/v1/item/{crawl_product_sku}/detail/top?isApp=false",
                                "responseMapping": "{}"
                            },
                       {
                                "endpointId": 21,
                                "stepOrder": 3,
                                "type": "CRAWLING",
                                "target": "PRODUCT",
                                "action": "SAVE_S3",
                                "params": {"siteProductId": "${crawl_product_sku}"},
                                "endPointUrl": "/legacy-api/v1/auction_products/{crawl_product_sku}/options",
                                "responseMapping": "{}"
                            }
                   ]
               }
           ],
           "headers": {
               "Accept": "*/*",
               "Connection": "close",
               "User-Agent": "Mozilla/5.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "ko-KR,ko;q=0.9"
           }
       }
       """

    data = json.loads(json_data)
    site_profile_response = SiteProfileResponse.from_dict(data)
    site_context = SiteContextResponse(site_id=1, site_name="MUSTIT", base_url="https://m.web.mustit.co.kr",
                                       country_code="KR", site_type="CRAWL", site_profiles=[site_profile_response])

    asyncio.run(crawl_task_executor.perform_crawling(
        site_profile=site_profile_response,
        site_context=site_context,
        task_info=site_profile_response.crawl_endpoints[0].crawl_tasks[0],
        previous_result={'content': [{'crawlProductId': 1, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95713119', 'productName': None, 'productGroupId': None}, {'crawlProductId': 2, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95713115', 'productName': None, 'productGroupId': None}, {'crawlProductId': 3, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711728', 'productName': None, 'productGroupId': None}, {'crawlProductId': 4, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711723', 'productName': None, 'productGroupId': None}, {'crawlProductId': 5, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711719', 'productName': None, 'productGroupId': None}, {'crawlProductId': 6, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711712', 'productName': None, 'productGroupId': None}, {'crawlProductId': 7, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711709', 'productName': None, 'productGroupId': None}, {'crawlProductId': 8, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711706', 'productName': None, 'productGroupId': None}, {'crawlProductId': 9, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711701', 'productName': None, 'productGroupId': None}, {'crawlProductId': 10, 'siteId': 1, 'siteName': 'MUSTIT', 'siteProductId': '95711699', 'productName': None, 'productGroupId': None}], 'last': True, 'first': False, 'sort': 'DESC', 'size': 10, 'numberOfElements': 10, 'empty': False, 'cursor': 10, 'totalElements': 180}
    ))
