import asyncio
import json
import logging
from typing import List

from injector import inject, singleton, Injector

from dataweave.aws.s3_upload_service import S3UploadService
from dataweave.gpt.models.processed_batch_data import ProcessedBatchData


@singleton
class BatchUploadManager:

    @inject
    def __init__(self, s3_upload_service: S3UploadService):
        self.s3_upload_service = s3_upload_service

    async def upload_batches(self, processed_data_list: List[ProcessedBatchData]):
        tasks = []

        for data in processed_data_list:
            json_data = json.dumps(data.content, ensure_ascii=False)
            tasks.append(self._upload_to_s3(json_data, data.object_name))

        await asyncio.gather(*tasks)

    async def _upload_to_s3(self, json_data: str, object_name: str):
        try:
            await self.s3_upload_service.upload_json_data(json_data, object_name)
            logging.info(f"Successfully uploaded data to S3 as {object_name}")
        except Exception as e:
            logging.error(f"Failed to upload data to S3: {e}")
            raise


injector = Injector()
batch_upload_manager = injector.get(BatchUploadManager)
