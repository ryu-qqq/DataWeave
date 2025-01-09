import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import List, TypeVar, Generic, Optional, Dict, Any


class PromptMetadata(ABC):

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_file_path(self) -> str:
        pass

    @staticmethod
    def get_custom_id() -> str:
        return uuid.uuid4().hex[:8]

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict[str, Any]) -> 'PromptMetadata':
        """Factory method to create an instance from a dictionary."""
        pass


@dataclass
class TestCodeMetadata(PromptMetadata):

    id: int
    commit_id: str
    class_name: str
    project_id: int
    branch_name: str
    file_path: str
    commit_message: str

    def get_id(self) -> int:
        return self.id

    def get_file_path(self) -> str:
        return self.file_path

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PromptMetadata':
        return TestCodeMetadata(
            id=data["id"],
            commit_id=data["commit_id"],
            class_name=data["class_name"],
            project_id=data["project_id"],
            branch_name=data["branch_name"],
            file_path=data["file_path"],
            commit_message=data["commit_message"]
        )


T = TypeVar("T", bound=PromptMetadata)


class Prompt(Generic[T]):
    def __init__(self, system_message: str, user_message: str, metadata: Optional[T]):
        self.system_message = system_message
        self.user_message = user_message
        self.metadata = metadata

    def to_message_list(self) -> List[dict]:
        return [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": self.user_message}
        ]

    def to_task(self, model: str, temperature: float, custom_id_prefix: str = "task") -> dict:
        return {
            "custom_id": f"{custom_id_prefix}-{self.metadata.get_custom_id()}-{self.metadata.get_file_path()}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model,
                "messages": self.to_message_list(),
                "temperature": temperature,
            },
        }
