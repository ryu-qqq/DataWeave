import asyncio
import logging
from typing import Optional, List, Any

from injector import singleton, inject, Injector

from dataweave.api_client.openai_client import OpenAIClient
from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.cache.batch_id_manager import BatchIdManager
from dataweave.enums.batch_status import BatchStatus
from dataweave.enums.product_data_type import ProductDataType
from dataweave.processor.batch_file_creator import BatchFileCreator
from dataweave.processor.batch_models import Batch
from dataweave.processor.token_counter import TokenCounter


@singleton
class BatchProcessor:
    @inject
    def __init__(self,
                 fetcher: ProductHubApiClient,
                 batch_file_creator: BatchFileCreator,
                 batch_id_manager: BatchIdManager,
                 openai_client: OpenAIClient):
        self.batch_id_manager = batch_id_manager
        self.fetcher = fetcher
        self.batch_file_creator = batch_file_creator
        self.openai_client = openai_client
        self.max_calls = 1

    def process(self, site_id: int, seller_id: int, page_size: int):
        all_data = []
        cursor: Optional[int] = None

        try:
            for call_count in range(self.max_calls):
                print(f"Fetching data (call {call_count + 1})...")
                slice_data = self.fetcher.fetch_product_group_processing_data(
                    site_id=site_id,
                    seller_id=seller_id,
                    cursor=cursor,
                    status='PROCESSING',
                    page_size=page_size
                )

                print(f"Fetched {len(slice_data.content)} items.")
                all_data.extend(slice_data.content)

                if slice_data.empty or slice_data.last:
                    print("No more data or last page reached.")
                    break

                cursor = slice_data.cursor
                print(f"Updated cursor: {cursor}")

            if not all_data:
                logging.warning("No data fetched for processing.")
                return

            print(f"Total items fetched: {len(all_data)}")
            self.process_chunk(all_data)

        except Exception as e:
            logging.error(f"Error during batch processing: {e}")
            raise

    def process_chunk(self, chunk: List[Any]):
        try:
            print("Processing current chunk...")

            for data_type in ProductDataType:
                print(f"Chunkifying data for data type: {data_type.value}")
                data_chunks = TokenCounter.chunkify_by_token_limit(
                    data=chunk,
                    model="gpt-4o-mini",
                    max_tokens=1500,
                    message_generator=self.batch_file_creator.create_message,
                    data_type=data_type
                )

                print(f"Split data into {len(data_chunks)} chunks for data type: {data_type.value}")

                for chunk_index, data_chunk in enumerate(data_chunks):
                    print(f"Processing chunk {chunk_index + 1}/{len(data_chunks)} for data type: {data_type.value}")
                    file_path = self.batch_file_creator.create_batch_file(data_chunk, data_type)
                    self.call_batch_api(data_type, file_path)

        except Exception as e:
            logging.error(f"Error processing chunk: {e}")
            raise

    def call_batch_api(self, data_type: ProductDataType, file_path: str):
        try:
            print("Uploading batch file to OpenAI...")
            upload_response = self.openai_client.upload_file(
                file_path=file_path,
                purpose="batch"
            )
            input_file_id = upload_response.id

            print("Creating batch job...")
            batch_response = self.openai_client.create_batch(
                input_file_id=input_file_id,
                endpoint="/v1/chat/completions",
                completion_window="24h"
            )

            batch_id = batch_response.id
            print(f"Batch API 호출 완료. Batch ID: {batch_id}")

            # Batch 객체 생성 및 저장
            batch = Batch(
                batch_id=batch_id,
                batch_name=batch_response.input_file_id,
                data_type=data_type,
                status=BatchStatus.PROCESSING,
                data={"input_file_id": input_file_id}
            )

            asyncio.run(self.batch_id_manager.save_batch(batch, expire=86400))

        except Exception as e:
            logging.error(f"Error during Batch API call: {e}")
            raise


injector = Injector()
batch_processor = injector.get(BatchProcessor)
