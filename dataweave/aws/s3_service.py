import json
import logging
import re

from io import BytesIO
from injector import inject, singleton, Injector
from dataweave.aws.aws_client import AWSClient


@singleton
class S3Service:

    @inject
    def __init__(self, aws_client: AWSClient):
        self.aws_client = aws_client

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

    async def download_json_data(self, object_name: str):
        if object_name.startswith("https://"):
            object_name = re.sub(r"^https://[^/]+/", "", object_name)

        async with await self.aws_client.create_s3_client() as s3_client:
            try:
                response = await s3_client.get_object(Bucket=self.aws_client.bucket_name, Key=object_name)
                data = await response['Body'].read()
                logging.info(f"JSON data downloaded from {self.aws_client.bucket_name}/{object_name}")
                return json.loads(data.decode('utf-8'))
            except Exception as e:
                logging.error(f"Failed to download JSON data from {self.aws_client.bucket_name}/{object_name}: {e}")
                raise

injector = Injector()
s3_service = injector.get(S3Service)
