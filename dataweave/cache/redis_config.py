import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class RedisConfig:
    def __init__(self):
        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")

        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        self.REDIS_DB = int(os.getenv("REDIS_DB", 0))
