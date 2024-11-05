import asyncio

from dataweave.api_client.google_search_api_client import google_search_api_client
from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.product_hub_api_client import product_hub_api_client
from dataweave.crawl_task_executor_service import CrawlTaskExecutorService
from dataweave.crawl_task_request import CrawlTaskRequest
from dataweave.crawler.auth.cookie_auth_provider import cookie_auth_provider

if __name__ == "__main__":
    task = CrawlTaskResponse(endpoint_id="1", step_order=1, task_type="NONE", action_target="",
                                 action_type="SAVE_S3", params="{}", response_mapping="{\"items\": \"$.items[*]\"}")

    headers = {
                    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                    "Accept": "text/html,application/xhtml+xml",
                    "Sec-Ch-Ua-Platform": "\"macOS\"",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
                    "Sec-Fetch-Site": "none",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9"
                }

    auth_settings = CrawlAuthSettingResponse(
        auth_type="COOKIE",
        auth_endpoint="https://m.web.mustit.co.kr",
        auth_headers="Authorization",
        auth_payload="\"${token_type} ${token}\""
    )

    request = CrawlTaskRequest(
        site_name="MUSTIT",
        crawl_type="API",
        base_url="https://m.web.mustit.co.kr",
        end_point_url="/mustit-api/facade-api/v1/search/mini-shop-search",
        parameters="sellerId=bino2345&pageNo={}&pageSize={}&order=LATEST",
        task=task,
        headers=headers,
        auth_settings=auth_settings,
        previous_result=None
    )


    asyncio.run(CrawlTaskExecutorService.do_task(request))
