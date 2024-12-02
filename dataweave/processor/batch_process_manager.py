import asyncio
import logging
import os
from typing import List, Dict, Any

from injector import singleton, inject, Injector

from dataweave.api_client.openai_client import OpenAIClient
from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.cache.batch_id_manager import BatchIdManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.processor.batch_data_mapper import BatchDataMapper
from dataweave.processor.batch_models import Batch
from dataweave.processor.batch_product_models import BatchProductModel


@singleton
class BatchProcessorManager:

    @inject
    def __init__(self,
                 batch_id_manager: BatchIdManager,
                 batch_data_mapper: BatchDataMapper,
                 openai_client: OpenAIClient,
                 product_hub_client: ProductHubApiClient):
        self.batch_data_mapper = batch_data_mapper
        self.base_dir = os.path.join(os.getcwd(), "batch", "completed")
        os.makedirs(self.base_dir, exist_ok=True)
        self.openai_client = openai_client
        self.batch_id_manager = batch_id_manager
        self.product_hub_client = product_hub_client

    async def process_completed_batches(self):
        logging.info("Fetching and processing completed batches...")

        completed_batches = await self.batch_id_manager.list_batches_by_status(BatchStatus.FAILED)
        logging.info(f"Found {len(completed_batches)} completed batches.")

        for batch in completed_batches:
            try:
                logging.info(f"Processing batch ID: {batch.batch_id}...")
                processed_data = await self.process_batch_data(batch)

                for data in processed_data:
                    self.send_processed_data(data)

                await self.batch_id_manager.update_batch_status(batch, BatchStatus.SEND_SERVER)
            except Exception as e:
                logging.error(f"Error processing batch ID {batch.batch_id}: {e}")
                await self.batch_id_manager.update_batch_status(batch, BatchStatus.FAILED)
                continue

    async def process_batch_data(self, batch: Batch) -> List[BatchProductModel]:
        logging.info(f"Processing batch data for batch ID: {batch.batch_id}...")

        save_path = os.path.join(self.base_dir, f"{batch.batch_id}.json")
        await asyncio.to_thread(self.openai_client.download_results, batch.data["output_file_id"], save_path)

        batch_product_models = self.batch_data_mapper.extract_content(batch.data_type, save_path)

        logging.info(f"Processed data for batch ID: {batch.batch_id}: {batch_product_models}")
        return batch_product_models

    def send_processed_data(self, processed_data: BatchProductModel):
        self.product_hub_client.update_processing_products(processed_data)


injector = Injector()
batch_processor_manager = injector.get(BatchProcessorManager)
