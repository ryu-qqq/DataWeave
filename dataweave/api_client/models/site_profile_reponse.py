from typing import List

from dataweave.api_client.models.crawl_auth_setting_response import CrawlAuthSettingResponse
from dataweave.api_client.models.crawl_endpoint_response import CrawlEndpointResponse
from dataweave.api_client.models.crawl_setting_response import CrawlSettingResponse


class SiteProfileResponse:
    def __init__(self, crawl_setting: CrawlSettingResponse, crawl_auth_setting: CrawlAuthSettingResponse, crawl_endpoints: List[CrawlEndpointResponse]):
        self.crawl_setting = crawl_setting
        self.crawl_auth_setting = crawl_auth_setting
        self.crawl_endpoints = crawl_endpoints

    @staticmethod
    def from_dict(data: dict) -> 'SiteProfileResponse':
        return SiteProfileResponse(
            crawl_setting=CrawlSettingResponse.from_dict(data.get("crawlSetting", {})),
            crawl_auth_setting=CrawlAuthSettingResponse.from_dict(data.get("crawlAuthSetting", {})),
            crawl_endpoints=[CrawlEndpointResponse.from_dict(ep) for ep in data.get("crawlEndpoints", [])]
        )