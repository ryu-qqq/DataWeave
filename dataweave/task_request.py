from typing import Optional, Any

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse


class TaskRequest:
    def __init__(self, site_name: str, crawl_type: str, base_url:str, end_point_url: str,
                 parameters: str, task: CrawlTaskResponse, headers: dict, auth_settings: CrawlAuthSettingResponse,
                 previous_result: Optional[Any] = None):

        self.site_name = site_name
        self.crawl_type = crawl_type
        self.base_url = base_url
        self.end_point_url = end_point_url
        self.parameters = parameters
        self.task = task
        self.headers = headers
        self.auth_settings = auth_settings
        self.method = 'GET'
        self.previous_result = previous_result
