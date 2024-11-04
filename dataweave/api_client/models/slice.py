from typing import Dict, List, Type, TypeVar, Optional, Generic

T = TypeVar('T')


class Slice(Generic[T]):
    def __init__(self, content: List[T], last: bool, first: bool, sort: Optional[Dict], size: int,
                 number_of_elements: int, empty: bool, cursor: Optional[int], total_elements: Optional[int]):
        self.content = content
        self.last = last
        self.first = first
        self.sort = sort
        self.size = size
        self.number_of_elements = number_of_elements
        self.empty = empty
        self.cursor = cursor
        self.total_elements = total_elements

    @staticmethod
    def from_dict(data: Dict, item_type: Type[T]) -> 'Slice[T]':
        content = [item_type.from_dict(item) for item in data.get("content", [])]
        return Slice(
            content=content,
            last=data.get("last", False),
            first=data.get("first", True),
            sort=data.get("sort"),
            size=data.get("size", 0),
            number_of_elements=data.get("numberOfElements", 0),
            empty=data.get("empty", True),
            cursor=data.get("cursor"),
            total_elements=data.get("totalElements")
        )


