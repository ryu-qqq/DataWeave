from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ProcessedBatchData:
    batch_id: str
    data_type: str
    content: Dict[str, Any]
    object_name: str
