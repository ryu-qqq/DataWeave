import asyncio
import json

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.crawler.task.crawl_task_executor import CrawlTaskExecutor, crawl_task_executor
from dataweave.processor.batch_process_manager import batch_processor_manager
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse
from dataweave.api_client.models.site_context_response import SiteContextResponse
from dataweave.processor.batch_processor import batch_processor
from dataweave.processor.batch_status_checker import batch_status_checker

if __name__ == "__main__":
    #batch_processor.process(site_id=4, seller_id=31, page_size=500)
    #asyncio.run(batch_status_checker.check_and_update_batch_states())
    asyncio.run(batch_processor_manager.process_completed_batches())

