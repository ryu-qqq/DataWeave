from injector import singleton, inject, Injector

from modules.http_client.async_http_client import AsyncHttpClient


@singleton
class GitHubClient:

    @inject
    def __init__(self, http_client: AsyncHttpClient):
        self.__http_client = http_client
        self.__base_url = "https://raw.githubusercontent.com"

    async def get_file_content(self, owner: str, repository_name: str, file_path: str, branch: str) -> str:

        endpoint = f"{self.__base_url}/{owner}/{repository_name}/main/{file_path}?={branch}"

        headers = {"Content-Type": "application/json"}
        response = await self.__http_client.request("GET", endpoint, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            raise RuntimeError(f"Failed to fetch file content: {response.status_code} - {response.text}")


injector = Injector()
git_hub_client = injector.get(GitHubClient)
