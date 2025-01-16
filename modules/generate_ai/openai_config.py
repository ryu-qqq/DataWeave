import os

from dotenv import load_dotenv
from injector import singleton

@singleton
class OpenAiConfig:
    def __init__(self):
        env = os.getenv("ENVIRONMENT", "local")
        env_file = f".env.{env}"
        load_dotenv(env_file)

        self.API_KEY = os.getenv("GPT_ACCESS_KEY")


