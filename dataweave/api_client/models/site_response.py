
class SiteResponse:
    def __init__(self, site_id: int, site_name: str, base_url: str, country_code: str, site_type: str):
        self.site_id = site_id
        self.site_name = site_name
        self.base_url = base_url
        self.country_code = country_code
        self.site_type = site_type

    @staticmethod
    def from_dict(data: dict) -> 'SiteResponse':
        return SiteResponse(
            site_id=data.get("siteId"),
            site_name=data.get("siteName"),
            base_url=data.get("baseUrl"),
            country_code=data.get("countryCode"),
            site_type=data.get("siteType")
        )
