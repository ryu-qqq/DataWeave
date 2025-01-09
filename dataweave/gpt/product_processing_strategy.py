from injector import singleton, inject

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.gpt.batch_processing_strategy import BatchProcessingStrategy
from dataweave.gpt.models.batch_models import Batch
from dataweave.gpt.models.product_models import BatchProductModel


@singleton
class ProductProcessingStrategy(BatchProcessingStrategy):

    @inject
    def __init__(self, product_hub_client: ProductHubApiClient):
        self.product_hub_client = product_hub_client

    async def process(self, batch: Batch):
        #batch_product_models = BatchDataMapper.extract_content(batch.data_type, save_path)

        processed_files = []
        # for model in batch_product_models:
        #     self.send_processed_data(model)
        #     processed_files.append(
        #         ProcessedBatchData(
        #             batch_id=batch.batch_id,
        #             data_type="product_title",
        #             content=model.to_dict(),
        #             object_name=f"batch/product/{batch.batch_id}/{model.product_group_id}.json",
        #         )
        #     )


    def send_processed_data(self, processed_data: BatchProductModel):
        self.product_hub_client.update_processing_products(processed_data)