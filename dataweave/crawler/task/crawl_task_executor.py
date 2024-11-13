import logging
from typing import Any

from injector import singleton, Injector, inject

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.action.action_provider import ActionProvider
from dataweave.crawler.auth.auth_provider import AuthProvider
from dataweave.crawler.auth.crawl_auth_manager import CrawlAuthManager
from dataweave.crawler.crawler_provider import CrawlerProvider


@singleton
class CrawlTaskExecutor:

    @inject
    def __init__(self, auth_manager: CrawlAuthManager):
        self.auth_manager = auth_manager

    async def perform_crawling(
            self, site_profile: SiteProfileResponse, site_context: SiteContextResponse,
            task_info: CrawlTaskResponse, previous_result: Any):

        crawl_type = site_profile.crawl_setting.crawl_type

        auth_headers = await self.auth_manager.authenticate(site_profile)
        crawler = CrawlerProvider.get_crawler(crawl_type)

        try:
            logging.info(f"Starting crawl for endpoint {task_info.endpoint_id} with {crawl_type} type.")
            crawl_data = await crawler.crawl(
                site_name=site_context.site_name,
                base_url=site_context.base_url,
                endpoint=task_info.end_point_url,
                parameters=task_info.params,
                headers=auth_headers,
                method="GET",
                response_mapping=task_info.response_mapping
            )

            logging.info(f"Crawl completed for endpoint {task_info.endpoint_id}")

            action_type = task_info.action
            action_provider = ActionProvider.get_action_provider(action_type)

            result = await action_provider.action(
                site_id=site_context.site_id,
                site_name=site_context.site_name,
                data=crawl_data,
                task=task_info
            )

            return result

        except Exception as e:
            logging.error(f"Failed to perform crawling: {e}")
            raise e


injector = Injector()
crawl_task_executor = injector.get(CrawlTaskExecutor)
