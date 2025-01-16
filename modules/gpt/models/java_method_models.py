from dataclasses import dataclass
from typing import Dict, List


@dataclass
class JavaMethod:
    method_name: str
    return_type: str
    parameters: List[Dict[str, str]]
    return_type_fields: Dict[str, str]

