import asyncio

from modules.spring_core_server.git.git_fetcher import spring_git_fetcher
from modules.spring_core_server.git.models.git_enums import GitType
from modules.spring_core_server.git.models.request.pull_request_filter import PullRequestFilterDto
from modules.spring_core_server.models.spring_enums import Sort


async def main():

    # PullRequestFilterDto 생성
    filter_dto = PullRequestFilterDto(
        git_type=GitType.GIT_HUB,
        status=None,
        review_status=None,
        page_size=10,
        page_number=0,
        cursor_id=None,
        sort=Sort.ASC
    )

    # Fetch pull requests
    pull_requests = await spring_git_fetcher.fetch_pull_request_files(15)

    # 결과 출력
    print("Fetched Pull Requests:")
    for pull_request in pull_requests:
        print(pull_request.to_dict())


if __name__ == "__main__":
    asyncio.run(main())