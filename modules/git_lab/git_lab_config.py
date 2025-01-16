import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class GitLabConfig:
    def __init__(self):
        env = os.getenv("ENVIRONMENT", "local")
        env_file = f".env.{env}"
        load_dotenv(env_file)

        self.BASE_URL = os.getenv("GIT_LAB_BASE_URL")
        self.TOKEN = os.getenv("GIT_LAB_TOKEN")
