import json

from injector import singleton, inject

from dataweave.api_client.models.site_profile_reponse import SiteProfileResponse
from dataweave.cache.redis_cache_manager import RedisCacheManager
from dataweave.crawler.auth.auth_provider import AuthProvider
from dataweave.crawler.auth.crawl_auth_context import CrawlAuthContext


@singleton
class CrawlAuthManager:

    @inject
    def __init__(self, auth_provider: AuthProvider, cache_manager: RedisCacheManager):
        self.auth_provider = auth_provider
        self.cache_manager = cache_manager

    async def authenticate(self, site_profile: SiteProfileResponse) -> CrawlAuthContext:
        auth_type = site_profile.crawl_auth_setting.auth_type
        auth_endpoint = site_profile.crawl_auth_setting.auth_endpoint

        cache_key = f"{auth_type}:{auth_endpoint}"

        cached_auth = await self.cache_manager.get(cache_key)
        if cached_auth:
            auth_context = json.loads(cached_auth)
            return auth_context["headers"]

        headers = site_profile.headers
        auth_payload = site_profile.crawl_auth_setting.auth_payload
        auth_headers, ttl = await self.auth_provider.get_auth_provider(auth_type).authenticate(
            auth_endpoint=auth_endpoint,
            headers=headers,
            auth_header=site_profile.crawl_auth_setting.auth_headers,
            payload=auth_payload
        )

        auth_context = {"headers": auth_headers}
        await self.cache_manager.set(cache_key, json.dumps(auth_context), expire=ttl)
        return auth_headers
