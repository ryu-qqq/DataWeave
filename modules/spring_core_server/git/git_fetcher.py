from injector import singleton, Injector

from dataweave.api_client.models.slice import Slice
from modules.spring_core_server.git.models.request.pull_request_filter import PullRequestFilterDto
from modules.spring_core_server.git.models.response.pull_request_changed_file_response_dto import \
    PullRequestChangedFileResponseDto
from modules.spring_core_server.git.models.response.pull_request_summary_dto import PullRequestSummaryResponseDto
from modules.spring_core_server.spring_core_server_client import SpringCoreServerClient


@singleton
class SpringGitFetcher(SpringCoreServerClient):
    async def fetch_pull_requests(self, filter_dto: PullRequestFilterDto) -> Slice[PullRequestSummaryResponseDto]:

        endpoint = "/pull-requests"
        query_params = filter_dto.to_query_params()

        response = await self._make_request("GET", endpoint, headers=self._header, params=query_params)
        return Slice.from_dict(response, PullRequestSummaryResponseDto)

    async def fetch_pull_request_files(self, pull_request_id: int) -> list[PullRequestChangedFileResponseDto]:

        endpoint = f"/pull-requests/file/{pull_request_id}"

        response = await self._make_request("GET", endpoint, headers=self._header)

        return [
            PullRequestChangedFileResponseDto.from_dict(file_data) for file_data in response
        ]


injector = Injector()
spring_git_fetcher = injector.get(SpringGitFetcher)
