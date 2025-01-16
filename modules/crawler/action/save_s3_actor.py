import logging
from datetime import datetime
from typing import Any

from injector import inject, singleton, Injector

from modules.crawler.models.crawl_task_reponse import CrawlTaskResponse
from modules.crawler.models.site_context_response import SiteContextResponse
from modules.crawler.models.site_profile_reponse import SiteProfileResponse
from modules.aws.s3_service import S3Service
from modules.crawler.action.action_interface import ActionInterface


@singleton
class SaveS3Actor(ActionInterface):

    @inject
    def __init__(self, s3_upload_service: S3Service):
        self.s3_upload_service = s3_upload_service

    async def action(self, site_profile: SiteProfileResponse, site_context: SiteContextResponse,
                     task: CrawlTaskResponse, data: Any, previous_result: Any):

        site_name = site_context.site_name
        site_id = site_context.site_id

        data_with_metadata = {
            "metadata": {"site_id": site_id, "site_name": site_name, "actionTarget": task.target},
            "data": data
        }

        object_name = self.__generate_object_name(site_name, task.target, task.endpoint_id)

        try:
            await self.s3_upload_service.upload_json_data(data_with_metadata, object_name)
            logging.info(f"Data successfully saved to S3: {object_name}")
        except Exception as e:
            logging.error(f"Failed to save data to S3: {e}")
            raise

    @staticmethod
    def __generate_object_name(site_name: str, target: str, endpoint_id: int) -> str:
        return f"CRAWLING/{target}/{site_name}/{endpoint_id}/{datetime.utcnow().strftime('data_%Y-%m-%d_%H-%M-%S.json')}"


injector = Injector()
save_s3_actor = injector.get(SaveS3Actor)
