import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class ProductHubConfig:
    def __init__(self):
        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")

        self.BASE_URL = os.getenv("PRODUCT_HUB_BASE_URL")
        self.API_KEY = os.getenv("PRODUCT_HUB_API_KEY")
