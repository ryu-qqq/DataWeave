from dataclasses import dataclass
from typing import List


@dataclass
class ProductData:
    id: int
    product_group_name: str
    brand_name: str
    categories: List[str]
    products: List[str]