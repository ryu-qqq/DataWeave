import os

from dotenv import load_dotenv
from injector import singleton


@singleton
class SpringCoreServerConfig:
    def __init__(self):
        env = os.getenv("ENVIRONMENT", "local")
        env_file = f".env.{env}"
        load_dotenv(env_file)

        self.BASE_URL = os.getenv("SPRING_CORE_SERVER_BASE_URL")
        self.API_KEY = os.getenv("SPRING_CORE_SERVER_API_KEY")

        if not self.BASE_URL or not self.API_KEY:
            raise ValueError("SPRING_CORE_SERVER_BASE_URL or SPRING_CORE_SERVER_API_KEY is not defined in the environment file")
