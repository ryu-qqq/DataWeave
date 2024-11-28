from dataclasses import asdict
from dataclasses import dataclass, field
from typing import Optional, Any, Dict

from dataweave.enums.batch_status import BatchStatus
from dataweave.enums.product_data_type import ProductDataType


@dataclass
class Batch:
    batch_id: str
    batch_name: str
    data_type: ProductDataType
    status: BatchStatus = BatchStatus.PROCESSING
    data: Optional[Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        result = asdict(self)
        result['data_type'] = self.data_type.name if isinstance(self.data_type, ProductDataType) else self.data_type
        result['status'] = self.status.name if isinstance(self.status, BatchStatus) else self.status
        return result

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Batch':
        return Batch(
            batch_id=data["batch_id"],
            batch_name=data["batch_name"],
            data_type=ProductDataType[data["data_type"]] if isinstance(data["data_type"], str) else data["data_type"],
            status=BatchStatus[data["status"]] if isinstance(data["status"], str) else data["status"],
            data=data.get("data", {})
        )

    def update_status(self, new_status: BatchStatus):
        self.status = new_status

    def is_completed(self) -> bool:
        return self.status == BatchStatus.COMPLETED

    def is_failed(self) -> bool:
        return self.status == BatchStatus.FAILED




