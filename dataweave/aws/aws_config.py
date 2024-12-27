import os
#
# from airflow.models import Variable
# from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from dotenv import load_dotenv
from injector import singleton


@singleton
class AwsConfig:
    # def __init__(self):
    #     aws_hook = AwsBaseHook(aws_conn_id="aws_default", client_type="s3")
    #     self.credentials = aws_hook.get_credentials()
    #     self.region_name = aws_hook.region_name
    #     self.bucket_name = Variable.get("bucket_name")

    def __init__(self):
        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")

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

