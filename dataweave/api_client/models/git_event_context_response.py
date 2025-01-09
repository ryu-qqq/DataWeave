from dataclasses import dataclass
from typing import List, Optional

from dataweave.api_client.git_lab_client import GitLabClient


@dataclass
class ChangedFile:
    git_event_id: int
    commit_id: str
    commit_message: str
    file_path: str
    change_type: str
    status: str
    file_content: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "ChangedFile":
        return ChangedFile(
            git_event_id=data["gitEventId"],
            commit_id=data["commitId"],
            commit_message=data["commitMessage"],
            file_path=data["filePath"],
            change_type=data["changeType"],
            status=data["status"],
        )

    async def load_content(self, gitlab_client: GitLabClient, project_id: int, branch_name: str):
        if self.file_content is None:
            self.file_content = await gitlab_client.get_file_content(
                project_id=project_id, file_path=self.file_path, ref=branch_name
            )


@dataclass
class GitEvent:
    id: int
    branch_name: str
    project_id: int
    repository_name: str
    status: str

    @staticmethod
    def from_dict(data: dict) -> "GitEvent":
        return GitEvent(
            id=data["id"],
            branch_name=data["branchName"],
            project_id=data["projectId"],
            repository_name=data["repositoryName"],
            status=data["status"],
        )


@dataclass
class GitEventContextResponse:
    git_event: GitEvent
    change_files: List[ChangedFile]

    @staticmethod
    def from_dict(data: dict) -> "GitEventContextResponse":
        return GitEventContextResponse(
            git_event=GitEvent.from_dict(data["gitEvent"]),
            change_files=[ChangedFile.from_dict(cf) for cf in data.get("changeFiles", [])]
        )
