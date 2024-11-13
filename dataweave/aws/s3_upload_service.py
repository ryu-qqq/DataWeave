import json
import logging

from io import BytesIO
from injector import inject, singleton, Injector
from dataweave.aws.aws_client import AWSClient


@singleton
class S3UploadService:

    @inject
    def __init__(self, aws_client: AWSClient):
        self.aws_client = aws_client
        self.aws_client = None


    async def upload_json_data(self, data, object_name):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)

        data_bytes = BytesIO(data.encode('utf-8'))

        async with await self.aws_client.create_s3_client() as s3_client:
            try:
                await s3_client.put_object(Bucket=self.aws_client.bucket_name, Key=object_name, Body=data_bytes)
                logging.info(f"JSON data uploaded to {self.aws_client.bucket_name}/{object_name}")
            except Exception as e:
                logging.error(f"Failed to upload JSON data to {self.aws_client.bucket_name}/{object_name}: {e}")
                raise


injector = Injector()
s3_upload_service = injector.get(S3UploadService)
