import json
import logging

from openai import Client
from openai import File

from injector import singleton, inject

from dataweave.api_client.openai_config import OpenAiConfig


@singleton
class OpenAIClient:

    @inject
    def __init__(self, config: OpenAiConfig):
        self.client = Client(api_key=config.API_KEY)

    def upload_file(self, file_path: str, purpose) -> File:
        with open(file_path, "rb") as f:
            response = self.client.files.create(file=f, purpose=purpose)
        return response

    def create_batch(self, input_file_id: str, endpoint, completion_window, metadata: dict = None):
        response = self.client.batches.create(
            input_file_id=input_file_id,
            endpoint=endpoint,
            completion_window=completion_window,
            metadata=metadata or {}
        )
        return response

    def retrieve_batch_status(self, batch_id: str):
        response = self.client.batches.retrieve(batch_id)
        return response

    def download_results(self, output_file_id: str, save_path: str) -> None:
        try:
            logging.info(f"Downloading output for file ID: {output_file_id}...")

            response = self.client.files.content(output_file_id)

            with open(save_path, "wb") as f:
                f.write(response.read())
            logging.info(f"Output saved to {save_path}")

        except Exception as e:
            logging.error(f"Failed to download output for file ID {output_file_id}: {e}")
            raise


    def list_batches(self, limit: int = 10) -> dict:
        response = self.client.batches.list(limit=limit)
        return response
