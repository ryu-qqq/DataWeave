
class CrawlAuthSettingResponse:
    def __init__(self, auth_type: str, auth_endpoint: str, auth_headers: str, auth_payload: str):
        self.auth_type = auth_type
        self.auth_endpoint = auth_endpoint
        self.auth_headers = auth_headers
        self.auth_payload = auth_payload

    def __repr__(self):
        return (f"CrawlAuthSettingResponse(auth_type='{self.auth_type}', auth_endpoint='{self.auth_endpoint}', "
                f"auth_headers='{self.auth_headers}', auth_payload='{self.auth_payload}')")

    @staticmethod
    def from_dict(data: dict) -> 'CrawlAuthSettingResponse':
        return CrawlAuthSettingResponse(
            auth_type=data.get("authType"),
            auth_endpoint=data.get("authEndpoint"),
            auth_headers=data.get("authHeaders"),
            auth_payload=data.get("authPayload")
        )