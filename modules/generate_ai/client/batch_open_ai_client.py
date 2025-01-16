import logging

from injector import singleton, inject
from openai import Client
from openai import File

from modules.open_ai.client.open_ai_client import OpenAiClient
from modules.open_ai.openai_config import OpenAiConfig


@singleton
class BatchOpenAIClient(OpenAiClient):
    """
    Batch OpenAI client for managing batch processing jobs.
    """

    @inject
    def __init__(self, config: OpenAiConfig):
        self.client = Client(api_key=config.API_KEY)

    def upload_file(self, file_path: str, purpose: str) -> File:
        """
        Uploads a file to OpenAI for processing.

        :param file_path: Path to the file.
        :param purpose: Purpose of the file (e.g., "fine-tune").
        :return: File object.
        """
        with open(file_path, "rb") as f:
            response = self.client.files.create(file=f, purpose=purpose)
        return response

    def create_batch(self, input_file_id: str, endpoint: str, completion_window: int) -> dict:
        """
        Creates a batch processing job.

        :param input_file_id: ID of the input file.
        :param endpoint: Target endpoint for processing.
        :param completion_window: Time window for completion.
        :return: Batch job details.
        """
        response = self.client.batches.create(
            input_file_id=input_file_id,
            endpoint=endpoint,
            completion_window=completion_window,
        )
        return response

    def retrieve_batch_status(self, batch_id: str) -> dict:
        """
        Retrieves the status of a batch job.

        :param batch_id: Batch ID.
        :return: Batch status details.
        """
        return self.client.batches.retrieve(batch_id)

    def download_results(self, file_id: str, save_path: str) -> None:
        """
        Downloads the results of a batch job.

        :param file_id: ID of the file to download.
        :param save_path: Local path to save the downloaded file.
        """
        try:
            logging.info(f"Downloading output for file ID: {file_id}...")
            response = self.client.files.content(file_id)
            with open(save_path, "wb") as f:
                f.write(response.read())
            logging.info(f"Output saved to {save_path}")
        except Exception as e:
            logging.error(f"Failed to download output for file ID {file_id}: {e}")
            raise

    def generate_prompt(self, system_message: str, user_message: str, model: str, temperature: float) -> str:
        """
        Generates a response for a batch processing use case (stub for this example).

        :param system_message: Context or instructions for the AI.
        :param user_message: User's input message.
        :param model: OpenAI model to use (e.g., "gpt-4").
        :param temperature: Sampling temperature.
        :return: AI-generated response.
        """
        # Batch prompt logic if required; for now, using a stub
        return "Batch processing is not yet implemented for prompt generation."
