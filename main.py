import asyncio

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.crawl_task_executor import CrawlTaskExecutor

if __name__ == "__main__":



    end_point = CrawlEndpointResponse(endpoint_id=1, end_point_url="/products/search", parameters="categoryNos=791683&order.direction=DESC&pageNumber={}&pageSize={}", crawl_tasks=[])

    headers = {
                    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                    "Accept": "*/*",
                    "Sec-Ch-Ua-Platform": "\"macOS\"",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.9"
                }

    auth_settings = CrawlAuthSettingResponse(
        auth_type="NONE",
        auth_endpoint="",
        auth_headers="",
        auth_payload="{\"version\": \"1.0\", \"clientid\": \"183SVEgDg5nHbILW//3jvg==\", \"platform\": \"PC\"}"
    )

    site_context = SiteContextResponse(site_id=2, site_name="KASINA", base_url="https://shop-api.e-ncp.com",
                                   country_code="KR", site_type="CRAWL", site_profiles= [])

    task = CrawlTaskResponse(endpoint_id="1", step_order=1, type="CRAWLING", target="RAW_DATA", action="SAVE_S3",
                                 params="{}", response_mapping="{\"items\": \"$.items[*]\"}")

    asyncio.run(CrawlTaskExecutor.perform_crawling(
        crawl_type="API",
        headers=headers,
        site_context= site_context,
        auth_settings=auth_settings,
        crawl_end_point=end_point,
        task_info=task
        ))
