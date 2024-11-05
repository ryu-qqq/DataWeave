import logging

from dataweave.crawl_task_request import CrawlTaskRequest
from dataweave.crawler.action.action_provider import ActionProvider
from dataweave.crawler.auth.auth_provider import AuthProvider
from dataweave.crawler.crawler_provider import CrawlerProvider


class CrawlTaskExecutorService:

    @staticmethod
    async def do_task(request: CrawlTaskRequest):
        logging.info(f"Processing task: {request.task.task_type} for site: {request.site_name}")

        auth_provider = AuthProvider.get_auth_provider(request.auth_settings.auth_type)

        headers = await auth_provider.authenticate(
            auth_endpoint=request.auth_settings.auth_endpoint,
            headers=request.headers,
            auth_header=request.auth_settings.auth_headers,
            payload=request.auth_settings.auth_payload
        )

        crawler = CrawlerProvider.get_crawler(request.crawl_type)

        data = await crawler.crawl(
            site_name=request.site_name,
            base_url=request.base_url,
            endpoint=request.end_point_url,
            parameters=request.parameters,
            method=request.method,
            headers=headers,
            response_mapping=request.task.response_mapping
        )

        actor = ActionProvider.get_action_provider(request.task.action_type)

        await actor.action(
            site_name=request.site_name,
            data=data
        )
