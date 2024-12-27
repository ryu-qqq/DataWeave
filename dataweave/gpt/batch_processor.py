import logging
from typing import List, Any, Dict

from injector import singleton, inject, Injector

from dataweave.api_client.openai_client import OpenAIClient
from dataweave.cache.batch_id_manager import BatchIdManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.enums.product_data_type import BatchDataType
from dataweave.enums.source_type import SourceType
from dataweave.gpt.batch_file_creator import BatchFileCreator
from dataweave.gpt.batch_models import Batch
from dataweave.gpt.data_fetcher_strategy_factory import DataFetcherStrategyFactory
from dataweave.gpt.data_mapper_provider_factory import DataMapperFactory
from dataweave.gpt.token_counter import TokenCounter


@singleton
class BatchProcessor:
    @inject
    def __init__(
        self,
        strategy_factory: DataFetcherStrategyFactory,
        data_mapper_factory: DataMapperFactory,
        batch_file_creator: BatchFileCreator,
        batch_id_manager: BatchIdManager,
        openai_client: OpenAIClient,
    ):
        self.strategy_factory = strategy_factory
        self.data_mapper_factory = data_mapper_factory
        self.batch_file_creator = batch_file_creator
        self.batch_id_manager = batch_id_manager
        self.openai_client = openai_client
        self.max_calls = 1

    async def process(
        self, source_type: SourceType, fetch_params: Dict[str, Any], batch_data_type: BatchDataType
    ):
        all_mapped_data = []
        current_cursor = fetch_params.pop("cursor", None)

        try:
            fetcher_strategy = self.strategy_factory.get_strategy(source_type)
            mapper = self.data_mapper_factory.get_mapper(source_type)

            for call_count in range(self.max_calls):
                logging.info(f"Fetching data (call {call_count + 1}) with cursor: {current_cursor}...")

                slice_data = fetcher_strategy.fetch_data(cursor=current_cursor, **fetch_params)

                if not slice_data.content:
                    logging.info("No data returned in this slice.")
                    break

                logging.info(f"Fetched {len(slice_data.content)} items.")

                for item in slice_data.content:
                    mapped_data = await mapper.map(item)
                    all_mapped_data.extend(mapped_data)

                if slice_data.empty or slice_data.last:
                    logging.info("No more data or last page reached.")
                    break

                current_cursor = slice_data.cursor
                fetch_params["cursor"] = current_cursor
                logging.info(f"Updated cursor: {current_cursor}")

            if not all_mapped_data:
                logging.warning("No data fetched for processing.")
                return

            logging.info(f"Total mapped items fetched: {len(all_mapped_data)}")
            await self.process_objects(all_mapped_data, batch_data_type)

        except Exception as e:
            logging.error(f"Error during batch processing: {e}")
            raise

    async def process_objects(self, objects: List[Any], batch_data_type: BatchDataType):
        try:
            logging.info("Processing objects for individual test generation...")

            prompts = await self.batch_file_creator.create_messages(objects, batch_data_type)

            for index, prompt in enumerate(prompts):
                logging.info(f"Processing object {index + 1}/{len(prompts)} for data type: {batch_data_type.value}")

                file_path, metadata = await self.batch_file_creator.create_batch_files(
                    [prompt], batch_data_type
                )

                await self.call_batch_api(batch_data_type, file_path, metadata)

        except Exception as e:
            logging.error(f"Error processing objects: {e}")
            raise

    async def call_batch_api(self, batch_data_type: BatchDataType, file_path: str, metadata: Dict[str, Any]):
        try:
            logging.info("Uploading batch file to OpenAI...")
            upload_response = self.openai_client.upload_file(
                file_path=file_path, purpose="batch"
            )
            input_file_id = upload_response.id

            logging.info("Creating batch job...")
            batch_response = self.openai_client.create_batch(
                input_file_id=input_file_id,
                endpoint="/v1/chat/completions",
                completion_window="24h",
            )

            batch_id = batch_response.id
            logging.info(f"Batch API 호출 완료. Batch ID: {batch_id}")

            batch = Batch(
                batch_id=batch_id,
                batch_name=batch_response.input_file_id,
                data_type=batch_data_type,
                status=BatchStatus.PROCESSING,
                data={"input_file_id": input_file_id},
                task_metadata=metadata,
            )

            await self.batch_id_manager.save_batch(batch, expire=86400)

        except Exception as e:
            logging.error(f"Error during Batch API call: {e}")
            raise


injector = Injector()
batch_processor = injector.get(BatchProcessor)
