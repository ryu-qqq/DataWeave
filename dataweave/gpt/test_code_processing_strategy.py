from injector import singleton

from dataweave.api_client.product_hub_api_client import ProductHubApiClient
from dataweave.enums.batch_status import BatchStatus
from dataweave.gpt.batch_processing_strategy import BatchProcessingStrategy
from dataweave.gpt.models.batch_models import Batch
from dataweave.gpt.models.prompt_models import TestCodeMetadata


@singleton
class TestCodeProcessingStrategy(BatchProcessingStrategy[TestCodeMetadata]):

    def __init__(self, product_hub_client: ProductHubApiClient):
        self.product_hub_client = product_hub_client

    async def process(self, batch: Batch[TestCodeMetadata]):
        metadata = batch.metadata
        git_id = metadata.get_id()
        self.product_hub_client.update_git_event_status(git_id, status=BatchStatus.COMPLETED.name)


