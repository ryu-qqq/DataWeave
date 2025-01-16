import asyncio
from typing import Dict

from dataweave.api_client.models.slice import Slice
from modules.cache_client.cursor_cache_manager import cursor_cache_manager
from modules.spring_core_server.git.git_commander import spring_git_commander
from modules.spring_core_server.git.git_fetcher import spring_git_fetcher
from modules.spring_core_server.git.models.git_enums import ReviewStatus
from modules.spring_core_server.git.models.request.pull_request_filter import PullRequestFilterDto
from modules.spring_core_server.git.models.response.pull_request_summary_dto import PullRequestSummaryResponseDto


async def update_review_status(pull_request_id: int, review_status: ReviewStatus):
    await spring_git_commander.update_pull_request_review_status_by_id(pull_request_id, review_status)


async def fetch_and_update_pull_requests_async() -> Dict:
    try:
        redis_key = "pull_requests_cursor"
        current_cursor = await cursor_cache_manager.get_cursor(redis_key)

        filter_dto = PullRequestFilterDto(
            status=None,
            review_status=ReviewStatus.PENDING,
            source_branch=None,
            target_branch=None,
            size=1,
            cursor=current_cursor,
        )

        pr_slice: Slice[PullRequestSummaryResponseDto] = await spring_git_fetcher.fetch_pull_requests(filter_dto)

        if pr_slice.empty:
            await cursor_cache_manager.set_cursor(redis_key, None)
            return {"content": [], "message": "No more pull requests to process."}

        new_cursor = pr_slice.cursor
        if new_cursor:
            await cursor_cache_manager.set_cursor(redis_key, new_cursor)

        update_tasks = [
            update_review_status(pr.id, ReviewStatus.IN_PROGRESS)
            for pr in pr_slice.content
        ]

        await asyncio.gather(*update_tasks)

        return pr_slice.to_dict()

    except Exception as e:
        raise RuntimeError(f"Failed to fetch and update pull requests: {e}")


def fetch_and_update_pull_requests(**kwargs) -> Dict:
    return asyncio.run(fetch_and_update_pull_requests_async())
