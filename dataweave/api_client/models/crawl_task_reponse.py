class CrawlTaskResponse:
    def __init__(self, endpoint_id: str, step_order: int, type: str, target: str, action: str,
                 params: str, response_mapping: str):
        self.endpoint_id = endpoint_id
        self.step_order = step_order
        self.type = type
        self.target = target
        self.action = action
        self.params = params
        self.response_mapping = response_mapping

    def __repr__(self):
        return (
            f"CrawlTaskResponse(endpoint_id='{self.endpoint_id}', step_order={self.step_order}, type='{self.type}', "
            f"target='{self.target}', action='{self.action}', params='{self.params}', "
            f"response_mapping='{self.response_mapping}')")


    @staticmethod
    def from_dict(data: dict) -> 'CrawlTaskResponse':
        return CrawlTaskResponse(
            endpoint_id=data.get("endpointId"),
            step_order=data.get("stepOrder"),
            type=data.get("type"),
            target=data.get("target"),
            action=data.get("action"),
            params=data.get("params"),
            response_mapping=data.get("responseMapping")
        )
