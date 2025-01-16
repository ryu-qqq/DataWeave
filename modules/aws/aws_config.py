import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class AwsConfig:
    def __init__(self):
        env = os.getenv("ENVIRONMENT", "local")
        env_file = f".env.{env}"
        load_dotenv(env_file)

        self.bucket_name = os.getenv("BUCKET_NAME")
        self.region_name = os.getenv("REGION_NAME", "ap-northeast-2")
        self.access_key = os.getenv("AWS_ACCESS_KEY")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    @property
    def aws_access_key(self):
        return self.access_key

    @property
    def aws_secret_access_key(self):
        return self.secret_key
