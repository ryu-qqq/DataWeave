from typing import List

from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.gpt.batch_data_mapper import BatchDataMapper
from dataweave.gpt.batch_models import Batch
from dataweave.gpt.batch_processing_strategy import BatchProcessingStrategy
from dataweave.gpt.batch_product_models import BatchProductModel
from dataweave.gpt.models.processed_batch_data import ProcessedBatchData


@singleton
class ProductProcessingStrategy(BatchProcessingStrategy):

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.product_hub_client = product_hub_client

    async def process_batch(self, batch: Batch, save_path: str) -> List[ProcessedBatchData]:
        batch_product_models = BatchDataMapper.extract_content(batch.data_type, save_path)

        processed_files = []
        for model in batch_product_models:
            self.send_processed_data(model)
            processed_files.append(
                ProcessedBatchData(
                    batch_id=batch.batch_id,
                    data_type="product_title",
                    content=model.to_dict(),
                    object_name=f"batch/product_title/{batch.batch_id}/{model.product_group_id}.json",
                )
            )

        return processed_files

    def send_processed_data(self, processed_data: BatchProductModel):
        self.product_hub_client.update_processing_products(processed_data)