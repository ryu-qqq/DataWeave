import asyncio
import logging
import os

from injector import singleton, inject, Injector

from dataweave.api_client.openai_client import OpenAIClient
from dataweave.enums.batch_status import BatchStatus
from dataweave.gpt.batch_id_manager import BatchIdManager
from dataweave.gpt.batch_processing_strategy_factory import BatchProcessingStrategyFactory
from dataweave.gpt.batch_upload_manager import BatchUploadManager
from dataweave.gpt.models.batch_models import Batch


@singleton
class CompletedBatchHandler:

    @inject
    def __init__(
        self,
        batch_processing_strategy_factory: BatchProcessingStrategyFactory,
        batch_id_manager: BatchIdManager,
        openai_client: OpenAIClient,
        batch_upload_manager: BatchUploadManager,
    ):
        self.__batch_processing_strategy_factory = batch_processing_strategy_factory
        self.__base_dir = os.path.join(os.getcwd(), "batch", "completed")
        os.makedirs(self.__base_dir, exist_ok=True)
        self.__openai_client = openai_client
        self.__batch_id_manager = batch_id_manager
        self.__batch_upload_manager = batch_upload_manager

    async def process_completed_batches(self):
        logging.info("Fetching and processing completed batches...")
        completed_batches = await self.__batch_id_manager.list_batches_by_status(BatchStatus.COMPLETED)

        if not completed_batches:
            logging.info("No completed batches to process.")
            return

        logging.info(f"Found {len(completed_batches)} completed batches.")
        await asyncio.gather(*(self._process_batch(batch) for batch in completed_batches))

    async def _process_batch(self, batch: Batch):
        try:
            s3_url = await self.__process_and_upload_batch(batch)
            await self.__update_batch_status(batch, BatchStatus.ENHANCED, s3_url=s3_url)
            logging.info(f"Batch {batch.batch_id} successfully processed and marked as ENHANCED.")
        except Exception as e:
            logging.error(f"Error processing batch {batch.batch_id}: {e}")
            await self.__update_batch_status(batch, BatchStatus.FAILED)

    async def __process_and_upload_batch(self, batch: Batch) -> str:
        logging.info(f"Starting processing for batch {batch.batch_id}...")

        strategy = self.__batch_processing_strategy_factory.get_strategy(batch.data_type)

        logging.info(f"Processing batch {batch.batch_id} with strategy {type(strategy).__name__}...")
        await strategy.process(batch)

        save_path = self.__get_save_path(batch.batch_id)

        self.__openai_client.download_results(batch.output_file_id, save_path)

        s3_url = await self.__batch_upload_manager.upload_and_cleanup(
            save_path, batch.batch_id, BatchStatus.ENHANCED.name
        )
        logging.info(f"Batch {batch.batch_id} uploaded to S3: {s3_url}")
        return s3_url

    async def __update_batch_status(self, batch: Batch, new_status: BatchStatus, s3_url: str = None):
        previous_status = batch.status
        batch.update_status(new_status)
        if s3_url:
            batch.update_s3_url(s3_url)
        await self.__batch_id_manager.update_batch(batch)
        logging.info(f"Batch {batch.batch_id} status updated: {previous_status} -> {new_status}")

    def __get_save_path(self, batch_id: str) -> str:
        return os.path.join(self.__base_dir, f"{batch_id}.json")


injector = Injector()
completed_batch_handler = injector.get(CompletedBatchHandler)
