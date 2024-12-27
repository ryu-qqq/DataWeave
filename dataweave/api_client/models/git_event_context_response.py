from dataclasses import dataclass
from typing import List, Optional

from dataweave.gitlab.git_lab_client import GitLabClient


@dataclass
class PublicMethod:
    public_method_id: int
    code_class_id: int
    method_name: str
    return_type: str
    parameter: str
    return_type_fields: str

    @staticmethod
    def from_dict(data: dict) -> "PublicMethod":
        return PublicMethod(
            public_method_id=data["publicMethodId"],
            code_class_id=data["codeClassId"],
            method_name=data["methodName"],
            return_type=data["returnType"],
            parameter=data["parameter"],
            return_type_fields=data["returnTypeFields"]
        )


@dataclass
class CodeClass:
    code_class_id: int
    change_file_id: int
    class_name: str
    requires_test: bool
    test_generate: bool
    public_methods: List[PublicMethod]

    @staticmethod
    def from_dict(data: dict) -> "CodeClass":
        return CodeClass(
            code_class_id=data["codeClassId"],
            change_file_id=data["changeFileId"],
            class_name=data["className"],
            requires_test=data["requiresTest"],
            test_generate=data["testGenerate"],
            public_methods=[PublicMethod.from_dict(pm) for pm in data.get("publicMethods", [])]
        )


@dataclass
class ChangedFile:
    git_event_id: int
    file_path: str
    change_type: str
    code_class: Optional[CodeClass]
    file_content: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "ChangedFile":
        return ChangedFile(
            git_event_id=data["gitEventId"],
            file_path=data["filePath"],
            change_type=data["changeType"],
            code_class=CodeClass.from_dict(data["codeClass"]) if "codeClass" in data else None
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
    commit_id: str
    commit_message: str
    repository_name: str
    status: str
    error_message: str

    @staticmethod
    def from_dict(data: dict) -> "GitEvent":
        return GitEvent(
            id=data["id"],
            branch_name=data["branchName"],
            project_id=data["projectId"],
            commit_id=data["commitId"],
            commit_message=data["commitMessage"],
            repository_name=data["repositoryName"],
            status=data["status"],
            error_message=data.get("errorMessage", "")
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
