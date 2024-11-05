import logging

from datetime import datetime
from typing import Any
from injector import inject, singleton, Injector
from dataweave.aws.s3_upload_service import S3UploadService
from dataweave.crawler.action.action_interface import ActionInterface


@singleton
class SaveS3ActionProvider(ActionInterface):

    @inject
    def __init__(self, s3_upload_service: S3UploadService):
        self.s3_upload_service = s3_upload_service

    async def action(self, site_name: str, data: Any):
        object_name = self.__generate_object_name(site_name)

        try:
            await self.s3_upload_service.upload_json_data(data, object_name)
            logging.info(f"Data successfully saved to S3: {object_name}")
        except Exception as e:
            logging.error(f"Failed to save data to S3: {e}")
            raise

    @staticmethod
    def __generate_object_name(site_name) -> str:
        return f"{site_name}/{datetime.utcnow().strftime('data_%Y-%m-%d_%H-%M-%S.json')}"

injector = Injector()
save_s3_action_provider = injector.get(SaveS3ActionProvider)

