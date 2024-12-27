from dataclasses import dataclass
from typing import Optional, List

from dataweave.gitlab.git_lab_client import GitLabClient


@dataclass
class PublicMethodDomain:
    method_name: str
    return_type: str
    parameters: List[dict]
    return_type_fields: dict


@dataclass
class CodeClassDomain:
    class_name: str
    requires_test: bool
    test_generate: bool
    public_methods: List[PublicMethodDomain]


@dataclass
class TestCodeData:
    branch_name: str
    project_id: int
    commit_id: str
    commit_message: str
    repository_name: str
    status: str
    error_message: str
    file_path: str
    change_type: str
    code_class: CodeClassDomain
    file_content: Optional[str] = None

    async def load_file_content(self, gitlab_client: GitLabClient):
        if self.file_content is None:
            self.file_content = await gitlab_client.get_file_content(
                project_id=self.project_id,
                file_path=self.file_path,
                ref=self.branch_name
            )
