from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional, Set

@dataclass
class BrandResponse:
    brand_id: int
    brand_name: str
    brand_name_kr: str
    brand_icon_image_url: str
    display_yn: bool

    @staticmethod
    def from_dict(data: dict) -> 'BrandResponse':
        return BrandResponse(
            brand_id=data["brandId"],
            brand_name=data["brandName"],
            brand_name_kr=data["brandNameKr"],
            brand_icon_image_url=data["brandIconImageUrl"],
            display_yn=data["displayYn"]
        )


@dataclass
class CategoryResponse:
    category_id: int
    category_name: str
    depth: int
    parent_category_id: int
    display_yn: bool
    target_group: str
    category_type: str
    path: str

    @staticmethod
    def from_dict(data: dict) -> 'CategoryResponse':
        return CategoryResponse(
            category_id=data["categoryId"],
            category_name=data["categoryName"],
            depth=data["depth"],
            parent_category_id=data["parentCategoryId"],
            display_yn=data["displayYn"],
            target_group=data["targetGroup"],
            category_type=data["categoryType"],
            path=data["path"]
        )


@dataclass
class OptionResponse:
    product_id: int
    option_group_id: int
    option_detail_id: int
    option_name: str
    option_value: str

    @staticmethod
    def from_dict(data: dict) -> 'OptionResponse':
        return OptionResponse(
            product_id=data["productId"],
            option_group_id=data["optionGroupId"],
            option_detail_id=data["optionDetailId"],
            option_name=data["optionName"],
            option_value=data["optionValue"]
        )


@dataclass
class ProductResponse:
    product_group_id: int
    product_id: int
    quantity: int
    sold_out_yn: bool
    display_yn: bool
    option: str
    options: List[OptionResponse]
    additional_price: Decimal

    @staticmethod
    def from_dict(data: dict) -> 'ProductResponse':
        return ProductResponse(
            product_group_id=data["productGroupId"],
            product_id=data["productId"],
            quantity=data["quantity"],
            sold_out_yn=data["soldOutYn"],
            display_yn=data["displayYn"],
            option=data["option"],
            options=[OptionResponse.from_dict(option) for option in data["options"]],
            additional_price=Decimal(data["additionalPrice"])
        )


@dataclass
class ProductGroupImageResponse:
    product_image_type: str
    image_url: str

    @staticmethod
    def from_dict(data: dict) -> 'ProductGroupImageResponse':
        return ProductGroupImageResponse(
            product_image_type=data["productImageType"],
            image_url=data["imageUrl"]
        )


@dataclass
class ProductNoticeResponse:
    material: str
    color: str
    size: str
    maker: str
    origin: str
    washing_method: str
    year_month: str
    assurance_standard: str
    as_phone: str

    @staticmethod
    def from_dict(data: dict) -> 'ProductNoticeResponse':
        return ProductNoticeResponse(
            material=data["material"],
            color=data["color"],
            size=data["size"],
            maker=data["maker"],
            origin=data["origin"],
            washing_method=data["washingMethod"],
            year_month=data["yearMonth"],
            assurance_standard=data["assuranceStandard"],
            as_phone=data["asPhone"]
        )


@dataclass
class ProductDeliveryResponse:
    delivery_area: str
    delivery_fee: Decimal
    delivery_period_average: int
    return_method_domestic: str
    return_courier_domestic: str
    return_charge_domestic: Decimal
    return_exchange_area_domestic: str

    @staticmethod
    def from_dict(data: dict) -> 'ProductDeliveryResponse':
        return ProductDeliveryResponse(
            delivery_area=data["deliveryArea"],
            delivery_fee=Decimal(data["deliveryFee"]),
            delivery_period_average=data["deliveryPeriodAverage"],
            return_method_domestic=data["returnMethodDomestic"],
            return_courier_domestic=data["returnCourierDomestic"],
            return_charge_domestic=Decimal(data["returnChargeDomestic"]),
            return_exchange_area_domestic=data["returnExchangeAreaDomestic"]
        )


@dataclass
class PriceResponse:
    regular_price: int
    current_price: int
    sale_price: int
    direct_discount_price: int
    direct_discount_rate: int
    discount_rate: int

    @staticmethod
    def from_dict(data: dict) -> 'PriceResponse':
        return PriceResponse(
            regular_price=data["regularPrice"],
            current_price=data["currentPrice"],
            sale_price=data["salePrice"],
            direct_discount_price=data["directDiscountPrice"],
            direct_discount_rate=data["directDiscountRate"],
            discount_rate=data["discountRate"]
        )


@dataclass
class ProductGroupResponse:
    product_group_id: int
    seller_id: int
    product_group_name: str
    style_code: str
    product_condition: str
    management_type: str
    option_type: str
    price: PriceResponse
    sold_out_yn: bool
    display_yn: bool
    product_status: str
    keywords: str
    product_delivery: Optional[ProductDeliveryResponse]
    product_notice: Optional[ProductNoticeResponse]
    product_detail_description: Optional[str]
    product_images: List[ProductGroupImageResponse]

    @staticmethod
    def from_dict(data: dict) -> 'ProductGroupResponse':
        return ProductGroupResponse(
            product_group_id=data["productGroupId"],
            seller_id=data["sellerId"],
            product_group_name=data["productGroupName"],
            style_code=data["styleCode"],
            product_condition=data["productCondition"],
            management_type=data["managementType"],
            option_type=data["optionType"],
            price=PriceResponse.from_dict(data["price"]),
            sold_out_yn=data["soldOutYn"],
            display_yn=data["displayYn"],
            product_status=data["productStatus"],
            keywords=data["keywords"],
            product_delivery=ProductDeliveryResponse.from_dict(data["productDelivery"]) if data.get("productDelivery") else None,
            product_notice=ProductNoticeResponse.from_dict(data["productNotice"]) if data.get("productNotice") else None,
            product_detail_description=data.get("productDetailDescription"),
            product_images=[
                ProductGroupImageResponse.from_dict(image) for image in data.get("productImages", [])
            ]
        )


@dataclass
class GptTrainingDataResponse:
    product_group: ProductGroupResponse
    products: List[ProductResponse]
    categories: List[CategoryResponse]
    brand: BrandResponse

    @staticmethod
    def from_dict(data: dict) -> 'GptTrainingDataResponse':
        return GptTrainingDataResponse(
            product_group=ProductGroupResponse.from_dict(data["productGroup"]),
            products=[ProductResponse.from_dict(product) for product in data["products"]],
            categories=[CategoryResponse.from_dict(category) for category in data["categories"]],
            brand=BrandResponse.from_dict(data["brand"])
        )