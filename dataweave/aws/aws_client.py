import logging

import aioboto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from injector import singleton, inject

from dataweave.aws.aws_config import AwsConfig


@singleton
class AWSClient:

    @inject
    def __init__(self, aws_config: AwsConfig):
        self.aws_config = aws_config
        self.bucket_name = aws_config.BUCKET_NAME

    async def create_s3_client(self):
        try:
            session = aioboto3.Session()
            async with session.client(
                's3',
                aws_access_key_id=self.aws_config.AWS_ACCESS_KEY,
                aws_secret_access_key=self.aws_config.AWS_SECRET_ACCESS_KEY,
                region_name=self.aws_config.REGION_NAME
            ) as client:
                return client  # 클라이언트를 반환
        except (NoCredentialsError, PartialCredentialsError) as e:
            logging.error(f"Error creating S3 client: {e}")
            raise
