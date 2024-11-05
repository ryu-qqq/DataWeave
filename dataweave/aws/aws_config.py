import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class AwsConfig:
    def __init__(self):
        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")

        self.AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.REGION_NAME = os.getenv("REGION_NAME")
        self.BUCKET_NAME = os.getenv("BUCKET_NAME")
