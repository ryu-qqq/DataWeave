from typing import List

from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse


class SiteContextResponse:
    def __init__(self, site_id: int, site_name: str, base_url: str, country_code: str, site_type: str, site_profiles: List[SiteProfileResponse]):
        self.site_id = site_id
        self.site_name = site_name
        self.base_url = base_url
        self.country_code = country_code
        self.site_type = site_type
        self.site_profiles = site_profiles

    @staticmethod
    def from_dict(data: dict) -> 'SiteContextResponse':
        return SiteContextResponse(
            site_id=data.get("siteId"),
            site_name=data.get("siteName"),
            base_url=data.get("baseUrl"),
            country_code=data.get("countryCode"),
            site_type=data.get("siteType"),
            site_profiles=[SiteProfileResponse.from_dict(ep) for ep in data.get("siteProfiles", [])]
        )