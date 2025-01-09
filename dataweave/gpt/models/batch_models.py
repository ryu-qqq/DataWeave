from dataclasses import dataclass, field
from typing import Optional, Any, Dict, TypeVar, Generic, Type

from dataweave.enums.batch_status import BatchStatus
from dataweave.enums.product_data_type import BatchDataType
from dataweave.gpt.models.prompt_models import PromptMetadata

T = TypeVar("T", bound=PromptMetadata)


@dataclass
class Batch(Generic[T]):
    batch_id: str
    file_id: str
    data_type: BatchDataType
    status: BatchStatus
    metadata: Optional[T]
    s3_url: Optional[str] = field(default=None)
    retry_count: int = field(default=0)
    max_retries: int = field(default=3)
    output_file_id: Optional[str] = None


    def to_dict(self) -> dict:
        result = {
            "batch_id": self.batch_id,
            "file_id": self.file_id,
            "data_type": self.data_type.name,
            "status": self.status.name,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "s3_url": self.s3_url,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "output_file_id" : self.output_file_id,
        }
        return result

    @staticmethod
    def from_dict(data: Dict[str, Any], metadata_class: Type[T]) -> 'Batch[T]':
        metadata_instance = None
        if data.get("metadata"):
            metadata_instance = metadata_class.from_dict(data["metadata"])

        return Batch(
            batch_id=data["batch_id"],
            file_id=data["file_id"],
            data_type=BatchDataType[data["data_type"]],
            status=BatchStatus[data["status"]],
            metadata=metadata_instance,
            s3_url=data.get("s3_url"),
            retry_count=data["retry_count"],
            max_retries=data["max_retries"],
            output_file_id=data.get("output_file_id"),
        )

    def update_status(self, new_status: BatchStatus):
        self.status = new_status

    def update_s3_url(self, s3_url: str):
        self.s3_url = s3_url

    def is_completed(self) -> bool:
        return self.status == BatchStatus.COMPLETED

    def is_failed(self) -> bool:
        return self.status == BatchStatus.FAILED


@dataclass
class BatchFile(Generic[T]):
    id: Optional[int]
    file_path: str
    metadata: Optional[T]


@dataclass
class ProcessedBatchData:
    batch_id: str
    data_type: BatchDataType
    content: Dict[str, Any]
    object_name: str
