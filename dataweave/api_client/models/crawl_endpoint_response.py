from typing import List

from dataweave.api_client.models.crawl_task_reponse import CrawlTaskResponse


class CrawlEndpointResponse:
    def __init__(self, end_point_url: str, crawl_tasks: List[CrawlTaskResponse]):
        self.end_point_url = end_point_url
        self.crawl_tasks = crawl_tasks

    @staticmethod
    def from_dict(data: dict) -> 'CrawlEndpointResponse':
        return CrawlEndpointResponse(
            end_point_url=data.get("endPointUrl"),
            crawl_tasks=[CrawlTaskResponse.from_dict(task) for task in data.get("crawlTasks", [])]
        )
