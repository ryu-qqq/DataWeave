import json
import logging
from typing import Any

from modules.crawler.models.crawl_task_reponse import CrawlTaskResponse
from modules.crawler.models.site_context_response import SiteContextResponse
from modules.crawler.models.site_profile_reponse import SiteProfileResponse
from modules.crawler.task.task_provider import TaskProvider


class TaskExecutor:
    def __init__(self, site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                 task_info: CrawlTaskResponse, previous_result: Any):
        self.site_profile = site_profile
        self.site_context = site_context
        self.task_info = task_info
        self.previous_result = previous_result

    async def execute(self):
        return await self._execute_processing_task()

    async def _execute_processing_task(self):
        logging.info(f"Executing PROCESSING task for endpoint {self.task_info.endpoint_id}")

        task_processor = TaskProvider.get_task_provider(self.task_info.type)
        result = await task_processor.processing(
            site_profile=self.site_profile,
            site_context=self.site_context,
            task_info=self.task_info,
            previous_result=self.previous_result
        )

        if hasattr(result, "to_dict"):
            return result.to_dict()
        else:
            try:
                return json.loads(json.dumps(result))
            except TypeError:
                raise ValueError("Result cannot be converted to JSON format")




