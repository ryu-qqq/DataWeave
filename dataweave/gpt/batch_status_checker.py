import logging
from typing import Optional

from injector import singleton, inject, Injector

from dataweave.gpt.batch_id_manager import BatchIdManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.gpt.batch_api_manager import BatchApiManager
from dataweave.gpt.models.batch_models import Batch


@singleton
class BatchStatusChecker:
    @inject
    def __init__(self, batch_api_manager: BatchApiManager, batch_id_manager: BatchIdManager):
        self.batch_api_manager = batch_api_manager
        self.batch_id_manager = batch_id_manager

    async def check_and_update_batch_states(self):
        logging.info("Checking batch states...")
        processing_batches = await self.batch_id_manager.list_batches_by_status(BatchStatus.PROCESSING)
        logging.info(f"Found {len(processing_batches)} batches to check.")

        completed_count = 0
        failed_count = 0

        for batch in processing_batches:
            try:
                status_response = await self.batch_api_manager.get_batch_status(batch.batch_id)
                status = status_response.status
                output_file_id = status_response.output_file_id

                if status == "completed":
                    await self._handle_completed(batch, output_file_id)
                    completed_count += 1
                elif status == "failed":
                    await self._handle_failed(batch)
                    failed_count += 1
                else:
                    logging.info(f"Batch {batch.batch_id} is still processing.")

            except Exception as e:
                logging.error(f"Error checking batch {batch.batch_id}: {e}")
                await self._update_batch_status(batch, BatchStatus.FAILED)
                failed_count += 1

        logging.info(f"Batch status check complete: {completed_count} completed, {failed_count} failed.")

    async def _handle_completed(self, batch: Batch, output_file_id: str):
        await self._update_batch_status(batch, BatchStatus.COMPLETED, output_file_id)
        logging.info(f"Batch {batch.batch_id} marked as COMPLETED.")

    async def _handle_failed(self, batch: Batch):
        if batch.retry_count < batch.max_retries:
            logging.warning(f"Batch {batch.batch_id} failed. Retrying... ({batch.retry_count + 1}/{batch.max_retries})")
            retry_response = await self._retry_batch(batch)
            batch.batch_id = retry_response.id
            await self._update_batch_status(batch, BatchStatus.PROCESSING)
        else:
            logging.error(f"Batch {batch.batch_id} has exhausted retries. Marking as EXHAUSTED.")
            await self._update_batch_status(batch, BatchStatus.EXHAUSTED)

    async def _retry_batch(self, batch: Batch):
        batch.retry_count += 1
        return await self.batch_api_manager.retry_batch(batch.file_id)

    async def _update_batch_status(self, batch: Batch, new_status: BatchStatus, output_file_id: Optional[str] = None):
        previous_status = batch.status
        batch.status = new_status
        if output_file_id:
            batch.output_file_id = output_file_id
        await self.batch_id_manager.update_batch(batch)
        logging.info(f"Batch {batch.batch_id} status updated: {previous_status} -> {new_status}")


injector = Injector()
batch_status_checker = injector.get(BatchStatusChecker)
