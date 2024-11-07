import os

from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from injector import singleton


@singleton
class AwsConfig:
    def __init__(self):
        aws_hook = AwsBaseHook(aws_conn_id="aws_default", client_type="s3")
        self.credentials = aws_hook.get_credentials()
        self.region_name = aws_hook.region_name
        self.bucket_name = Variable.get("bucket_name")

    @property
    def aws_access_key(self):
        return self.credentials.access_key

    @property
    def aws_secret_access_key(self):
        return self.credentials.secret_key

