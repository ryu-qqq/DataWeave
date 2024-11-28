import os

from dotenv import load_dotenv
from injector import singleton


@singleton
class OpenAiConfig:
    def __init__(self):

        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")

        self.API_KEY = os.getenv("GPT_ACCESS_KEY")
