

class GoogleSearchResponse:
    def __init__(self, site_id: int, site_name: str, base_url: str, country_code: str, site_type: str):
        self.site_id = site_id
        self.site_name = site_name
        self.base_url = base_url
        self.country_code = country_code
        self.site_type = site_type
