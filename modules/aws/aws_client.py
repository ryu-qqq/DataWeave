import logging

import aioboto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from injector import singleton, inject

from modules.aws.aws_config import AwsConfig


@singleton
class AWSClient:

    @inject
    def __init__(self, aws_config: AwsConfig):
        self.aws_config = aws_config
        self.bucket_name = aws_config.bucket_name

    async def create_s3_client(self):
        try:
            session = aioboto3.Session()
            return session.client(
                's3',
                aws_access_key_id=self.aws_config.aws_access_key,
                aws_secret_access_key=self.aws_config.aws_secret_access_key,
                region_name=self.aws_config.region_name
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            logging.error(f"Error creating S3 client: {e}")
            raise


