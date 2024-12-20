from typing import List, Dict

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.crawl_setting_response import CrawlSettingResponse


class SiteProfileResponse:
    def __init__(self, mapping_id: int, crawl_setting: CrawlSettingResponse,
                 crawl_auth_setting: CrawlAuthSettingResponse, crawl_endpoints: List[CrawlEndpointResponse],
                 headers: Dict[str, str]):
        self.mapping_id = mapping_id
        self.crawl_setting = crawl_setting
        self.crawl_auth_setting = crawl_auth_setting
        self.crawl_endpoints = crawl_endpoints
        self.headers = headers

    def __repr__(self):
        return (f"SiteProfileResponse(mapping_id={self.mapping_id}, crawl_setting={self.crawl_setting}, "
                f"crawl_auth_setting={self.crawl_auth_setting}, crawl_endpoints={self.crawl_endpoints}, "
                f"headers={self.headers})")

    @staticmethod
    def from_dict(data: dict) -> 'SiteProfileResponse':
        return SiteProfileResponse(
            mapping_id=data.get("mappingId", 0),
            crawl_setting=CrawlSettingResponse.from_dict(data.get("crawlSetting", {})),
            crawl_auth_setting=CrawlAuthSettingResponse.from_dict(data.get("crawlAuthSetting", {})),
            crawl_endpoints=[CrawlEndpointResponse.from_dict(ep) for ep in data.get("crawlEndpoints", [])],
            headers=data.get("headers", {})
        )
