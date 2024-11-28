from typing import Any

from injector import singleton, Injector

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.action.action_provider import ActionProvider
from dataweave.crawler.task.task_interface import TaskInterface


@singleton
class ProcessingTaskExecutor(TaskInterface):

    async def processing(self, **kwargs):
        return await self.perform_processing(**kwargs)

    @staticmethod
    async def perform_processing(site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                                 task_info: CrawlTaskResponse, previous_result: Any):

        provider = ActionProvider.get_action_provider(task_info.action)
        return await provider.action(
            site_profile=site_profile,
            site_context=site_context,
            task=task_info,
            previous_result=previous_result,
            data=None
        )


injector = Injector()
process_task_executor = injector.get(ProcessingTaskExecutor)
