import logging
from typing import List

import yaml

from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse


class SiteContextResponse:
    def __init__(self, site_id: int, site_name: str, base_url: str, country_code: str, site_type: str,
                 site_profiles: List[SiteProfileResponse]):
        self.site_id = site_id
        self.site_name = site_name
        self.base_url = base_url
        self.country_code = country_code
        self.site_type = site_type
        self.site_profiles = site_profiles

    def __repr__(self):
        return (f"SiteContextResponse(site_id={self.site_id}, site_name='{self.site_name}', "
                f"base_url='{self.base_url}', country_code='{self.country_code}', site_type='{self.site_type}', "
                f"site_profiles={self.site_profiles})")

    @staticmethod
    def from_dict(data: dict) -> 'SiteContextResponse':
        site_profiles_data = data.get("siteProfiles", [])
        site_profiles = [SiteProfileResponse.from_dict(profile) for profile in site_profiles_data]

        return SiteContextResponse(
            site_id=data.get("siteId"),
            site_name=data.get("siteName"),
            base_url=data.get("baseUrl"),
            country_code=data.get("countryCode"),
            site_type=data.get("siteType"),
            site_profiles=site_profiles
        )

    @staticmethod
    def load_site_config(file_path):
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        site_context = SiteContextResponse.from_dict(config)
        return site_context
