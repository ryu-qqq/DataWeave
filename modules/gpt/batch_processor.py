import inspect
import logging
from typing import List, Any, Dict

from injector import singleton, inject, Injector

from modules.gpt.models.batch_status import BatchStatus
from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.batch_api_manager import BatchApiManager
from modules.gpt.batch_file_creator import BatchFileCreator
from modules.gpt.batch_id_manager import BatchIdManager
from modules.gpt.batch_upload_manager import BatchUploadManager
from modules.gpt.data_fetcher_strategy_factory import DataFetcherStrategyFactory
from modules.gpt.data_mapper_provider_factory import DataMapperFactory
from modules.gpt.models.batch_models import Batch, BatchFile
from modules.utils.retry_utils import RetryUtils


@singleton
class BatchProcessor:
    @inject
    def __init__(
        self,
        strategy_factory: DataFetcherStrategyFactory,
        data_mapper_factory: DataMapperFactory,
        batch_file_creator: BatchFileCreator,
        batch_api_manager: BatchApiManager,
        batch_id_manager: BatchIdManager,
        batch_upload_manager: BatchUploadManager,
    ):
        self.__strategy_factory = strategy_factory
        self.__data_mapper_factory = data_mapper_factory
        self.__batch_file_creator = batch_file_creator
        self.__batch_api_manager = batch_api_manager
        self.__batch_id_manager = batch_id_manager
        self.__batch_upload_manager = batch_upload_manager
        self.__max_retries = 2

    async def process(self, fetch_params: Dict[str, Any], batch_data_type: BatchDataType):
        try:
            raw_data = await self.__fetch_data(fetch_params, batch_data_type)
            mapped_data = await self.__map_data(raw_data, batch_data_type)

            if not mapped_data:
                logging.warning("No data fetched for processing.")
                return

            await self.__process_objects(mapped_data, batch_data_type)
        except Exception as e:
            logging.error(f"Error during batch processing: {e}")
            raise

    async def __fetch_data(self, fetch_params: Dict[str, Any], batch_data_type: BatchDataType):
        fetcher_strategy = self.__strategy_factory.get_strategy(batch_data_type)
        logging.info("Fetching data...")
        if inspect.iscoroutinefunction(fetcher_strategy.fetch_data):
            return await fetcher_strategy.fetch_data()
        else:
            return fetcher_strategy.fetch_data(**fetch_params)

    async def __call_mapper(self, mapper, raw_data):
        if inspect.iscoroutinefunction(mapper.map):
            return await mapper.map(raw_data)
        else:
            return mapper.map(raw_data)

    async def __map_data(self, raw_data: List[Any], batch_data_type: BatchDataType) -> List[Any]:
        if not isinstance(raw_data, list):
            raise ValueError("Fetcher strategy must return a list.")

        mapper = self.__data_mapper_factory.get_mapper(batch_data_type)
        mapped_data = await self.__call_mapper(mapper, raw_data)  # Unified call
        logging.info(f"Total mapped items: {len(mapped_data)}")
        return mapped_data

    async def __process_objects(self, objects: List[Any], batch_data_type: BatchDataType):
        logging.info(f"Processing {len(objects)} objects for {batch_data_type.value}")
        batch_files = await self.__batch_file_creator.create_batch_files(objects, batch_data_type)

        for batch_file in batch_files:
            await RetryUtils.retry_with_backoff(
                self.__process_single_batch_file,
                max_retries=self.__max_retries,
                batch_file=batch_file,
                batch_data_type=batch_data_type,
            )

    async def __process_single_batch_file(self, batch_file: BatchFile, batch_data_type: BatchDataType):
        batch_response = await self.__batch_api_manager.create_batch(batch_file.file_path)

        batch = Batch(
            batch_id=batch_response.id,
            file_id=batch_response.input_file_id,
            data_type=batch_data_type,
            status=BatchStatus.PROCESSING,
            metadata=batch_file.metadata,
        )

        await self.__batch_id_manager.save_batch(batch)

        logging.info(f"Batch {batch.batch_id} created successfully.")

        await self.__batch_upload_manager.upload_and_cleanup(
            batch_file.file_path, batch.batch_id, BatchStatus.PROCESSING.name
        )


injector = Injector()
batch_processor = injector.get(BatchProcessor)
