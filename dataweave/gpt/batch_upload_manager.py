import json
import logging
import os

import aiofiles
from injector import inject, singleton, Injector

from dataweave.aws.s3_service import S3Service
from dataweave.file_manager import FileManager


@singleton
class BatchUploadManager:

    @inject
    def __init__(self, s3_upload_service: S3Service):
        self.__s3_upload_service = s3_upload_service
        self.__base_domain = "https://d3fej89xf1vai5.cloudfront.net"

    async def upload_and_cleanup(self, file_path: str, batch_id: str, status: str) -> str:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            file_content = await file.read()

        try:
            json_data = json.loads(file_content)
        except json.JSONDecodeError:
            raise ValueError(f"File at {file_path} contains invalid JSON content.")

        object_name = f"batch/test_code/{os.path.basename(file_path)}"
        await self.__s3_upload_service.upload_json_data(json_data, object_name)

        FileManager.cleanup_downloaded_file(file_path)
        s3_url = f"{self.__base_domain}/{batch_id}/{status}/{object_name}"
        logging.info(f"Uploaded and cleaned up file: {file_path}, S3 URL: {s3_url}")
        return s3_url


injector = Injector()
batch_upload_manager = injector.get(BatchUploadManager)
