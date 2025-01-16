from dataclasses import dataclass
from datetime import datetime

from modules.spring_core_server.git.models.git_enums import MergeStatus, ReviewStatus


@dataclass
class PullRequestSummaryResponseDto:
    id: int
    git_pull_id: int
    branch_id: int
    git_type: str
    source_branch: str
    target_branch: str
    title: str
    status: MergeStatus
    review_status: ReviewStatus
    create_at: datetime

    @staticmethod
    def from_dict(data: dict) -> "PullRequestSummaryResponseDto":
        return PullRequestSummaryResponseDto(
            id=data["id"],
            git_pull_id=data["gitPullId"],
            branch_id=data["branchId"],
            git_type=data["gitType"],
            source_branch=data["sourceBranch"],
            target_branch=data["targetBranch"],
            title=data["title"],
            status=MergeStatus.of(data["status"]),
            review_status=ReviewStatus[data["reviewStatus"]],
            create_at=datetime.fromisoformat(data["createAt"])
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "gitPullId": self.git_pull_id,
            "branchId": self.branch_id,
            "gitType": self.git_type,
            "sourceBranch": self.source_branch,
            "targetBranch": self.target_branch,
            "title": self.title,
            "status": self.status.value,
            "reviewStatus": self.review_status.value,
            "createAt": self.create_at.isoformat(),
        }