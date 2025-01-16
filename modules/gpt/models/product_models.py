from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

class BatchProductModel(ABC):

    def __init__(self, product_group_id: int, type: str):
        self.product_group_id = product_group_id
        self.type = type

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data: Dict[str, Any]) -> 'BatchProductModel':
        pass

@dataclass
class TitleResponse(BatchProductModel):
    type: str = "title"
    product_group_id: int = 0
    original_title: str = ""
    filtered_title: Dict[str, str] = None
    brand_name: str = ""
    style_code: str = ""
    color_in_title: str = ""
    deleted_words: list = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'TitleResponse':
        return cls(
            product_group_id=data.get("product_group_id", 0),
            original_title=data.get("original_title", ""),
            filtered_title=data.get("filtered_title", {}),
            brand_name=data.get("brand_name", ""),
            style_code=data.get("style_code", ""),
            color_in_title=data.get("color_in_title", ""),
            deleted_words=data.get("deleted_words", [])
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



@dataclass
class NormalizedOptions:
    sizes: List[str] = field(default_factory=list)
    unit: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NormalizedOptions':
        return cls(
            sizes=data.get("sizes", []),
            unit=data.get("unit", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OptionsResponse(BatchProductModel):
    type: str = "options"
    product_group_id: int = 0
    original_options: List[str] = field(default_factory=list)
    normalized_options: NormalizedOptions = field(default_factory=NormalizedOptions)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'OptionsResponse':
        return cls(
            product_group_id=data.get("product_group_id", 0),
            original_options=data.get("original_options", []),
            normalized_options=NormalizedOptions.from_dict(data.get("normalized_options", {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["normalized_options"] = self.normalized_options.to_dict()
        return result



@dataclass
class DescriptionResponse(BatchProductModel):
    type: str = "description"
    product_group_id: int = 0
    description: str = ""

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'DescriptionResponse':
        return cls(
            product_group_id=data.get("product_group_id", 0),
            description=data.get("description", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)