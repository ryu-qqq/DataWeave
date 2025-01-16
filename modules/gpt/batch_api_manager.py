import logging

from injector import singleton, inject

from modules.open_ai.openai_client import OpenAIClient


@singleton
class BatchApiManager:
    @inject
    def __init__(self, openai_client: OpenAIClient):
        self.__openai_client = openai_client

    async def create_batch(self, file_path: str, completion_window: str = "24h"):
        try:
            input_file_id = await self.__upload_file_for_batch(file_path)
            return await self.__initiate_batch(input_file_id, completion_window)
        except Exception as e:
            logging.error(f"Error creating batch for file: {file_path}, Error: {e}")
            raise

    async def retry_batch(self, input_file_id: str, completion_window: str = "24h"):
        try:
            return await self.__initiate_batch(input_file_id, completion_window)
        except Exception as e:
            logging.error(f"Error retrying batch with input_file_id: {input_file_id}, Error: {e}")
            raise

    async def get_batch_status(self, batch_id: str):

        try:
            logging.info(f"Retrieving status for batch ID: {batch_id}...")
            return self.__openai_client.retrieve_batch_status(batch_id)
        except Exception as e:
            logging.error(f"Error retrieving status for batch ID: {batch_id}, Error: {e}")
            raise

    async def __upload_file_for_batch(self, file_path: str) -> str:

        try:
            logging.info(f"Uploading batch file: {file_path}...")
            upload_response = self.__openai_client.upload_file(file_path, purpose="batch")
            logging.info(f"File uploaded successfully with ID: {upload_response.id}")
            return upload_response.id
        except Exception as e:
            logging.error(f"Error uploading batch file: {file_path}, Error: {e}")
            raise

    async def __initiate_batch(self, input_file_id: str, completion_window: str):

        try:
            logging.info(f"Initiating batch with input_file_id: {input_file_id}...")
            batch_response = self.__openai_client.create_batch(
                input_file_id=input_file_id,
                endpoint="/v1/chat/completions",
                completion_window=completion_window,
            )
            logging.info(f"Batch initiated successfully: {batch_response}")
            return batch_response
        except Exception as e:
            logging.error(f"Error initiating batch with input_file_id: {input_file_id}, Error: {e}")
            raise
