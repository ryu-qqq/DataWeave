import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class RedisConfig:
    def __init__(self):
        env = os.getenv("ENVIRONMENT", "local")
        env_file = f".env.{env}"
        load_dotenv(env_file)

        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        self.REDIS_DB = int(os.getenv("REDIS_DB", 0))


