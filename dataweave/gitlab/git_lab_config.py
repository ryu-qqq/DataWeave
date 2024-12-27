import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class GitLabConfig:
    def __init__(self):

        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")

        self.BASE_URL = os.getenv("GIT_LAB_BASE_URL")
        self.TOKEN = os.getenv("GIT_LAB_TOKEN")
