from typing import Any

from injector import singleton, Injector

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.action.action_provider import ActionProvider


@singleton
class ProcessingTaskExecutor:

    @staticmethod
    async def perform_processing(site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                                 task_info: CrawlTaskResponse, previous_result: Any):

        provider = ActionProvider.get_action_provider(task_info.action)
        return provider.action(site_name=site_context.site_name)


injector = Injector()
process_task_executor = injector.get(ProcessingTaskExecutor)
