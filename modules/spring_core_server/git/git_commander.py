import json

from injector import singleton, Injector

from modules.spring_core_server.git.models.git_enums import ReviewStatus
from modules.spring_core_server.spring_core_server_client import SpringCoreServerClient


@singleton
class SpringGitCommander(SpringCoreServerClient):

    async def update_pull_request_review_status_by_id(self, pull_request_id: int, review_status: ReviewStatus) :

        endpoint = f"/pull-requests/{pull_request_id}"

        request_body = {"review_status": review_status}
        await self._make_request("PATCH", endpoint, headers=self._header, data=json.dumps(request_body))



injector = Injector()
spring_git_commander = injector.get(SpringGitCommander)

