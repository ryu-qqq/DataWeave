import logging
from typing import Any

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.task.task_provider import TaskProvider


class TaskExecutor:
    def __init__(self, site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                 task_info: CrawlTaskResponse, previous_result: Any):
        self.site_profile = site_profile
        self.site_context = site_context
        self.task_info = task_info
        self.previous_result = previous_result

    async def execute(self):
        return self._execute_processing_task()

    async def _execute_processing_task(self):
        logging.info(f"Executing PROCESSING task for endpoint {self.task_info.endpoint_id}")

        task_processor = TaskProvider.get_task_provider(self.task_info.type)
        return await task_processor.processing(
            site_profile=self.site_profile,
            site_context=self.site_context,
            task_info=self.task_info,
            previous_result=self.previous_result
        )


