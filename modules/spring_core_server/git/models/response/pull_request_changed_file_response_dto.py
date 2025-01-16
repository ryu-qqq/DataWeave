from modules.spring_core_server.git.models.git_enums import ChangeType, ReviewStatus


class PullRequestChangedFileResponseDto:
    def __init__(
        self,
        repository_name: str,
        owner: str,
        pull_request_id: int,
        commit_id: int,
        changed_file_id: int,
        class_name: str,
        file_path: str,
        change_typ: ChangeType,
        review_status: ReviewStatus
    ):
        self.repository_name = repository_name
        self.owner = owner
        self.pull_request_id = pull_request_id
        self.commit_id = commit_id
        self.changed_file_id = changed_file_id
        self.class_name = class_name
        self.file_path = file_path
        self.change_typ = change_typ
        self.review_status = review_status

    @staticmethod
    def from_dict(data: dict) -> 'PullRequestChangedFileResponseDto':
        return PullRequestChangedFileResponseDto(
            repository_name=data["repositoryName"],
            owner=data["owner"],
            pull_request_id=data["pullRequestId"],
            commit_id=data["commitId"],
            changed_file_id=data["changedFileId"],
            class_name=data["className"],
            file_path=data["filePath"],
            change_typ=ChangeType[data["changeTyp"]],
            review_status=ReviewStatus[data["reviewStatus"]]
        )

    def to_dict(self) -> dict:
        return {
            "repositoryName": self.repository_name,
            "owner": self.owner,
            "pullRequestId": self.pull_request_id,
            "commitId": self.commit_id,
            "changedFileId": self.changed_file_id,
            "className": self.class_name,
            "filePath": self.file_path,
            "changeTyp": self.change_typ.name,
            "reviewStatus": self.review_status.name
        }
