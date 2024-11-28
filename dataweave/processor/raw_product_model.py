from dataclasses import dataclass
from typing import Optional, List

from dataweave.api_client.models.product_group_context_response import ProductGroupProcessingDataResponse


@dataclass
class SlimProductGroup:
    product_group_id: int
    original_product_name: str
    brand_name: str
    style_code: Optional[str]
    color: Optional[str]
    categories: List[str]
    options: List[str]
    price: int
    country_codes: List[str]

    @staticmethod
    def from_product_group(item: ProductGroupProcessingDataResponse) -> 'SlimProductGroup':
        product_group = item.product_group
        return SlimProductGroup(
            product_group_id=product_group.product_group_id,
            original_product_name=product_group.product_group_name,
            brand_name=product_group.brand.brand_name if product_group.brand else "",
            style_code=product_group.style_code,
            color=None,  # Color is derived later in the process
            categories=[category.category_name for category in product_group.categories],
            options=[product.option for product in item.products],
            price=product_group.price.current_price,
            country_codes=[external.country_code for external in item.external_mall_product_pending_data],
        )
