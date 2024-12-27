from dataclasses import dataclass
from typing import List


@dataclass
class ProductData:
    product_group_id: int
    product_group_name: str
    brand_name: str
    categories: List[str]
    products: List[str]