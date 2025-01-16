from typing import List

from modules.crawler.models.crawl_task_reponse import CrawlTaskResponse


class CrawlEndpointResponse:
    def __init__(self, endpoint_id: int, end_point_url: str, parameters: str, crawl_tasks: List[CrawlTaskResponse]):
        self.endpoint_id = endpoint_id
        self.end_point_url = end_point_url
        self.parameters = parameters
        self.crawl_tasks = crawl_tasks

    def __repr__(self):
        return (f"CrawlEndpointResponse(endpoint_id={self.endpoint_id}, end_point_url='{self.end_point_url}', "
                f"parameters='{self.parameters}', crawl_tasks={self.crawl_tasks})")

    @staticmethod
    def from_dict(data: dict) -> 'CrawlEndpointResponse':
        return CrawlEndpointResponse(
            endpoint_id=data.get("endpointId"),
            end_point_url=data.get("endPointUrl"),
            parameters=data.get("parameters"),
            crawl_tasks=[CrawlTaskResponse.from_dict(task, data.get("endPointUrl")) for task in data.get("crawlTasks", [])]
        )
