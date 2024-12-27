import asyncio
import json

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.task.crawl_task_executor import CrawlTaskExecutor, crawl_task_executor
from dataweave.enums.product_data_type import BatchDataType
from dataweave.enums.source_type import SourceType
from dataweave.gpt.batch_process_manager import batch_processor_manager
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.gpt.batch_processor import batch_processor
from dataweave.gpt.batch_status_checker import batch_status_checker




if __name__ == "__main__":
    #asyncio.run(batch_status_checker.check_and_update_batch_states())
    asyncio.run(batch_processor_manager.process_completed_batches())

    asyncio.run(batch_processor.process(
        source_type=SourceType.TEST_CODE,
        fetch_params={
            "status": "PENDING",
            "change_types": ["ADDED", "MODIFIED"],
            "page_size": 20,
            "page_number": 0,
            "cursor": None,
            "sort": "ASC"
        },
        batch_data_type=BatchDataType.TEST_CODE
    ))

