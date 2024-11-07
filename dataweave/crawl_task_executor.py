import logging
from typing import Dict
from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.crawler.action.action_provider import ActionProvider
from dataweave.crawler.auth.auth_provider import AuthProvider
from dataweave.crawler.crawler_provider import CrawlerProvider


class CrawlTaskExecutor:

    @staticmethod
    async def perform_crawling(crawl_type: str, headers: Dict[str, str],
                               site_context: SiteContextResponse,
                               auth_settings: CrawlAuthSettingResponse,
                               crawl_end_point: CrawlEndpointResponse, task_info: CrawlTaskResponse):

        crawler = CrawlerProvider.get_crawler(crawl_type)
        auth_provider = AuthProvider.get_auth_provider(auth_settings.auth_type)

        auth_headers = await auth_provider.authenticate(
            auth_endpoint=auth_settings.auth_endpoint,
            headers=headers,
            auth_header=auth_settings.auth_headers,
            payload=auth_settings.auth_payload
        )

        try:
            logging.info(f"Starting crawl for endpoint {task_info.endpoint_id} with {crawl_type} type.")
            crawl_data = await crawler.crawl(
                site_name=site_context.site_name,
                base_url=site_context.base_url,
                endpoint=crawl_end_point.end_point_url,
                parameters=crawl_end_point.parameters,
                headers=auth_headers,
                method="GET",
                response_mapping=task_info.response_mapping
            )

            logging.info(f"Crawl completed for endpoint {task_info.endpoint_id}")

            action_type = task_info.action
            action_provider = ActionProvider.get_action_provider(action_type)
            result = await action_provider.action(site_name=site_context.site_name, data=crawl_data, task=task_info)
            return result

        except Exception as e:
            logging.error(f"Failed to perform crawling: {e}")
            raise e
