import logging

from injector import singleton, inject, Injector

from dataweave.api_client.openai_client import OpenAIClient
from dataweave.cache.batch_id_manager import BatchIdManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.gpt.batch_models import Batch


@singleton
class BatchStateChecker:

    @inject
    def __init__(self,
                 batch_id_manager: BatchIdManager,
                 openai_client: OpenAIClient):

        self.batch_id_manager = batch_id_manager
        self.openai_client = openai_client

    async def check_and_update_batch_states(self):
        logging.info("Checking batch states...")
        processing_batches = await self.batch_id_manager.list_batches_by_status(BatchStatus.PROCESSING)
        logging.info(f"Found {len(processing_batches)} batches to check.")

        for batch in processing_batches:
            try:
                status_response = self.openai_client.retrieve_batch_status(batch.batch_id)

                logging.info(f"Batch ID {batch.batch_id} status: {status_response}")

                if status_response.status == "completed":
                    output_file_id = status_response.output_file_id

                    if not output_file_id:
                        raise ValueError(f"No output_file_id found for batch {batch.batch_id}")

                    batch.data = batch.data or {}
                    batch.data["output_file_id"] = output_file_id
                    await self.batch_id_manager.update_batch_status(batch, BatchStatus.PROCESSING)

                    logging.info(f"Batch {batch.batch_id} completed with output_file_id {output_file_id}.")

                elif status_response.status == "failed":
                    logging.warning(f"Batch {batch.batch_id} failed. Retrying...")
                    await self.retry_batch(batch)

                else:
                    print(f"Batch {batch.batch_id} not yet completed.")

            except Exception as e:
                logging.error(f"Error checking batch {batch.batch_id}: {e}")
                await self.batch_id_manager.update_batch_status(batch, BatchStatus.FAILED)

    async def retry_batch(self, batch: Batch):
        try:
            logging.info(f"Retrying batch {batch.batch_id}...")

            input_file_id = batch.data.get("input_file_id")
            if not input_file_id:
                raise ValueError(f"No input_file_id found for batch {batch.batch_id}")

            retry_response = self.openai_client.create_batch(
                input_file_id=input_file_id,
                endpoint="/v1/chat/completions",
                completion_window="24h"
            )

            new_batch_id = retry_response.id
            logging.info(f"Batch {batch.batch_id} retried with new batch ID {new_batch_id}.")

            await self.batch_id_manager.delete_batch(batch)
            batch.batch_id = new_batch_id
            batch.status = BatchStatus.PROCESSING
            await self.batch_id_manager.save_batch(batch)

        except Exception as e:
            logging.error(f"Error retrying batch {batch.batch_id}: {e}")
            await self.batch_id_manager.update_batch_status(batch, BatchStatus.FAILED)


injector = Injector()
batch_status_checker = injector.get(BatchStateChecker)
