import os
from dotenv import load_dotenv
from injector import singleton


@singleton
class GoogleSearchConfig:
    def __init__(self):
        ENV = os.getenv("ENVIRONMENT", "local")
        if ENV == "dev":
            load_dotenv(".env.dev")
        elif ENV == "prod":
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.local")
        self.BASE_URL = os.getenv("GOOGLE_SEARCH_URL")
        self.API_KEY = os.getenv("GOOGLE_SEARCH_API")
        self.URL = f"{self.BASE_URL}?key={self.API_KEY}&cx=44d600842a2b74ed7&q="
