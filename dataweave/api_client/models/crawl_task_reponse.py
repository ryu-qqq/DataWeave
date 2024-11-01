class CrawlTaskResponse:
    def __init__(self, endpoint_id: str, step_order: int, task_type: str, action_target: str, action_type: str,
                 params: str, response_mapping: str):
        self.endpoint_id = endpoint_id
        self.step_order = step_order
        self.task_type = task_type
        self.action_target = action_target
        self.action_type = action_type
        self.params = params
        self.response_mapping = response_mapping

    @staticmethod
    def from_dict(data: dict) -> 'CrawlTaskResponse':
        return CrawlTaskResponse(
            endpoint_id=data.get("endpointId"),
            step_order=data.get("stepOrder"),
            task_type=data.get("taskType"),
            action_target=data.get("actionTarget"),
            action_type=data.get("actionType"),
            params=data.get("params"),
            response_mapping=data.get("responseMapping")
        )
