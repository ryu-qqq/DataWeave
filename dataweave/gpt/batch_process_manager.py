import asyncio
import logging
import os

from injector import singleton, inject, Injector

from dataweave.api_client.openai_client import OpenAIClient
from dataweave.cache.batch_id_manager import BatchIdManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.gpt.batch_models import Batch
from dataweave.gpt.batch_processing_strategy_factory import BatchProcessingStrategyFactory
from dataweave.gpt.batch_upload_manager import BatchUploadManager


@singleton
class BatchProcessorManager:

    @inject
    def __init__(self,
                 batch_processing_strategy_factory: BatchProcessingStrategyFactory,
                 batch_id_manager: BatchIdManager,
                 openai_client: OpenAIClient,
                 batch_upload_manager: BatchUploadManager,
                 ):
        self.batch_processing_strategy_factory = batch_processing_strategy_factory
        self.base_dir = os.path.join(os.getcwd(), "batch", "completed")
        os.makedirs(self.base_dir, exist_ok=True)
        self.openai_client = openai_client
        self.batch_id_manager = batch_id_manager
        self.batch_upload_manager = batch_upload_manager

    async def process_completed_batches(self):
        logging.info("Fetching and processing completed batches...")
        completed_batches = await self.batch_id_manager.list_batches_by_status(BatchStatus.PROCESSING)
        logging.info(f"Found {len(completed_batches)} completed batches.")

        if not completed_batches:
            logging.info("No completed batches to process.")
            return

        await asyncio.gather(*(self._process(batch) for batch in completed_batches))

    async def _process(self, batch: Batch):
        try:
            processed_data = await self.process_batch_data(batch)
            await self.batch_upload_manager.upload_batches(processed_data)
            await self.batch_id_manager.update_batch_status(batch, BatchStatus.COMPLETED)
        except Exception as e:
            logging.error(f"Error while processing Completed Batch : {e}")
            await self.batch_id_manager.update_batch_status(batch, BatchStatus.FAILED)

    async def process_batch_data(self, batch: Batch) -> list:
        strategy = self.batch_processing_strategy_factory.get_strategy(batch.data_type)
        save_path = await self.download_batch_results(batch)
        processed_data = await strategy.process_batch(batch, save_path)
        return processed_data

    async def download_batch_results(self, batch: Batch) -> str:
        save_path = os.path.join(self.base_dir, f"{batch.batch_id}.json")
        await asyncio.to_thread(self.openai_client.download_results, batch.data["output_file_id"], save_path)
        logging.info(f"Downloaded batch results to {save_path} for batch ID: {batch.batch_id}")
        return save_path


injector = Injector()
batch_processor_manager = injector.get(BatchProcessorManager)
