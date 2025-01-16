import logging
import urllib.parse

from injector import singleton, inject

from modules.http_client.async_http_client import AsyncHttpClient
from modules.git_lab.git_lab_config import GitLabConfig


@singleton
class GitLabClient:

    @inject
    def __init__(self, git_lab_config: GitLabConfig, http_client: AsyncHttpClient):
        self.base_url = git_lab_config.BASE_URL
        self.token = git_lab_config.TOKEN
        self.http_client = http_client

    async def create_merge_request(self, project_id: int, source_branch: str, target_branch: str, title: str):
        url = f"{self.base_url}/projects/{project_id}/merge_requests"
        headers = {"Private-Token": self.token, "Content-Type": "application/json"}
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
        }

        logging.info(f"Creating merge request: {data}")
        response = await self.http_client.request("POST", url, headers=headers, json=data)
        return response

    async def push_file(self, project_id: int, file_path: str, branch: str, content: str, commit_message: str):
        url = f"{self.base_url}/projects/{project_id}/repository/files/{file_path}"
        headers = {"Private-Token": self.token, "Content-Type": "application/json"}
        data = {
            "branch": branch,
            "content": content,
            "commit_message": commit_message,
        }

        logging.info(f"Pushing file {file_path} to branch {branch}...")
        response = await self.http_client.request("POST", url, headers=headers, json=data)
        return response

    async def get_project_id(self, project_name: str):
        url = f"{self.base_url}/projects"
        headers = {"Private-Token": self.token}

        response = await self.http_client.request("GET", url, headers=headers, params={"search": project_name})
        projects = response.json()
        for project in projects:
            if project["name"] == project_name:
                return project["id"]
        raise ValueError(f"Project {project_name} not found.")

    async def get_file_content(self, project_id: int, file_path: str, ref: str) -> str:
        encoded_file_path = urllib.parse.quote(file_path, safe="")
        url = f"{self.base_url}/projects/{project_id}/repository/files/{encoded_file_path}/raw"
        headers = {"Private-Token": self.token}
        params = {"ref": ref}

        logging.info(f"Fetching content for file {file_path} in project {project_id} at ref {ref}")
        response = await self.http_client.request("GET", url, headers=headers, params=params)
        return response

    async def create_file_specific_branch(self, project_id: int, base_branch: str, file_path: str):
        branch_name = f"{base_branch}-{hash(file_path)}"
        url = f"{self.base_url}/projects/{project_id}/repository/branches"
        headers = {"Private-Token": self.token}
        data = {
            "branch": branch_name,
            "ref": base_branch
        }
        response = await self.http_client.request("POST", url, headers=headers, json=data)
        return branch_name
