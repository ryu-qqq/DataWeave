import logging
from typing import Any
from injector import singleton, Injector, inject
from modules.crawler.models.crawl_task_reponse import CrawlTaskResponse
from modules.crawler.models.site_context_response import SiteContextResponse
from modules.crawler.models.site_profile_reponse import SiteProfileResponse
from modules.crawler.action.action_provider import ActionProvider
from modules.crawler.auth.crawl_auth_manager import CrawlAuthManager
from modules.crawler.crawler_provider import CrawlerProvider
from modules.crawler.task.task_interface import TaskInterface

@singleton
class CrawlTaskExecutor(TaskInterface):

    async def processing(self, **kwargs):
        return await self.perform_crawling(**kwargs)

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

            if previous_result:
                site_product_ids = [item["siteProductId"] for item in previous_result['content']]

                results = []
                for site_product_id in site_product_ids:
                    endpoint_url = task_info.end_point_url.replace("{crawl_product_sku}", str(site_product_id))

                    crawl_data = await crawler.crawl(
                        site_name=site_context.site_name,
                        base_url=site_context.base_url,
                        endpoint=endpoint_url,
                        parameters="",
                        headers=auth_headers,
                        method="GET",
                        response_mapping=task_info.response_mapping
                    )

                    action_type = task_info.action
                    action_provider = ActionProvider.get_action_provider(action_type)

                    result = await action_provider.action(
                        site_profile=site_profile,
                        site_context=site_context,
                        data=crawl_data,
                        task=task_info,
                        previous_result=previous_result
                    )

                    results.append(result)

                logging.info(f"Crawl completed for multiple endpoints in {task_info.endpoint_id}")
                return results

            else:
                crawl_data = await crawler.crawl(
                    site_name=site_context.site_name,
                    base_url=site_context.base_url,
                    endpoint=task_info.end_point_url,
                    parameters=task_info.params,
                    headers=auth_headers,
                    method="GET",
                    response_mapping=task_info.response_mapping
                )

                action_type = task_info.action
                action_provider = ActionProvider.get_action_provider(action_type)

                result = await action_provider.action(
                    site_profile=site_profile,
                    site_context=site_context,
                    data=crawl_data,
                    task=task_info,
                    previous_result=previous_result
                )

                logging.info(f"Crawl completed for single endpoint in {task_info.endpoint_id}")
                return result

        except Exception as e:
            logging.error(f"Failed to perform crawling: {e}")
            raise e


injector = Injector()
crawl_task_executor = injector.get(CrawlTaskExecutor)
