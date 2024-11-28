class CrawlTaskResponse:
    def __init__(self, endpoint_id: int, step_order: int, type: str, target: str, action: str,
                 params: str, end_point_url: str, response_mapping: str):
        self.endpoint_id = endpoint_id
        self.step_order = step_order
        self.type = type
        self.target = target
        self.action = action
        self.params = params
        self.end_point_url = end_point_url
        self.response_mapping = response_mapping

    def __repr__(self):
        return (
            f"CrawlTaskResponse(endpoint_id='{self.endpoint_id}', step_order={self.step_order}, type='{self.type}', "
            f"target='{self.target}', action='{self.action}', params='{self.params}', endpointUrl='{self.end_point_url}', "
            f"response_mapping='{self.response_mapping}')")

    @staticmethod
    def from_dict(data: dict, end_point_url: str = "") -> 'CrawlTaskResponse':
        final_end_point_url = end_point_url + data.get("endPointUrl") if end_point_url else data.get("endPointUrl")

        return CrawlTaskResponse(
            endpoint_id=data.get("endpointId"),
            step_order=data.get("stepOrder"),
            type=data.get("type"),
            target=data.get("target"),
            action=data.get("action"),
            params=data.get("params"),
            end_point_url=final_end_point_url,
            response_mapping=data.get("responseMapping")
        )
