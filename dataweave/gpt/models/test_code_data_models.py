from dataclasses import dataclass
from typing import Optional

from dataweave.api_client.git_lab_client import GitLabClient


@dataclass
class TestCodeData:
    id: int
    branch_name: str
    project_id: int
    commit_id: str
    commit_message: str
    repository_name: str
    status: str
    file_path: str
    change_type: str
    file_content: Optional[str] = None

    async def load_file_content(self, gitlab_client: GitLabClient):
        if self.file_content is None:
            self.file_content = await gitlab_client.get_file_content(
                project_id=self.project_id,
                file_path=self.file_path,
                ref=self.branch_name
            )
