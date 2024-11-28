import unittest
from decimal import Decimal

from dataweave.api_client.models.product_group_context_response import ProductGroupProcessingDataResponse

MOCK_PRODUCT_GROUP_DATA = {
    "productGroup": {
        "productGroupId": 1,
        "sellerId": 101,
        "color": {"colorId": 1, "colorName": "Red"},
        "categories": [
            {
                "id": 1,
                "categoryName": "women",
                "depth": 1,
                "parentCategoryId": 0,
                "displayYn": True,
                "targetGroup": "FEMALE",
                "categoryType": "NONE",
                "path": "1"
            }
        ],
        "brand": {
            "id": 1,
            "brandName": "BrandX",
            "brandNameKr": "",
            "brandIconImageUrl": "https://brandx.com/logo.png",
            "displayYn": True
        },
        "productGroupName": "Sample Product Group",
        "styleCode": "SGX001",
        "productCondition": "NEW",
        "managementType": "MANUAL",
        "optionType": "OPTION_TWO",
        "price": {
            "regularPrice": 100000,
            "currentPrice": 50000,
            "salePrice": 50000,
            "directDiscountPrice": 50000,
            "directDiscountRate": 50,
            "discountRate": 50
        },
        "soldOutYn": False,
        "displayYn": True,
        "productStatus": "WAITING",
        "keywords": "",
        "config": {
            "productGroupConfig": {"configId": 1, "productGroupId": 1, "activeYn": True},
            "productGroupNameConfigs": [{"countryCode": "US", "customName": ""}]
        }
    },
    "products": [
        {
            "productGroupId": 1,
            "productId": 1,
            "quantity": 10,
            "soldOutYn": False,
            "displayYn": True,
            "option": "",
            "options": [
                {"productId": 1, "optionGroupId": 1, "optionDetailId": 1, "optionName": "COLOR", "optionValue": "Black"},
                {"productId": 1, "optionGroupId": 2, "optionDetailId": 2, "optionName": "SIZE", "optionValue": "M"}
            ],
            "additionalPrice": 0
        },
        {
            "productGroupId": 1,
            "productId": 2,
            "quantity": 5,
            "soldOutYn": False,
            "displayYn": True,
            "option": "",
            "options": [
                {"productId": 2, "optionGroupId": 1, "optionDetailId": 1, "optionName": "COLOR", "optionValue": "Black"},
                {"productId": 2, "optionGroupId": 2, "optionDetailId": 3, "optionName": "SIZE", "optionValue": "L"}
            ],
            "additionalPrice": 0
        }
    ],
    "externalMallProductPendingData": [
        {"siteId": 1, "productGroupId": 1, "policyId": 1, "countryCode": "US", "translatedNeeded": True}
    ]
}


class TestProductGroupProcessingDataResponse(unittest.TestCase):
    def test_product_group_from_dict(self):
        # 데이터 변환
        product_group_processing_data = ProductGroupProcessingDataResponse.from_dict(MOCK_PRODUCT_GROUP_DATA)

        # ProductGroupResponse 검증
        product_group = product_group_processing_data.product_group
        self.assertEqual(product_group.product_group_id, 1)
        self.assertEqual(product_group.seller_id, 101)
        self.assertEqual(product_group.product_group_name, "Sample Product Group")
        self.assertEqual(product_group.style_code, "SGX001")
        self.assertEqual(product_group.product_condition, "NEW")
        self.assertEqual(product_group.management_type, "MANUAL")
        self.assertEqual(product_group.option_type, "OPTION_TWO")
        self.assertFalse(product_group.sold_out_yn)
        self.assertTrue(product_group.display_yn)
        self.assertEqual(product_group.product_status, "WAITING")

        # Color 검증
        self.assertEqual(product_group.color.color_id, 1)
        self.assertEqual(product_group.color.color_name, "Red")

        # Categories 검증
        self.assertEqual(len(product_group.categories), 1)
        category = product_group.categories[0]
        self.assertEqual(category.id, 1)
        self.assertEqual(category.category_name, "women")
        self.assertEqual(category.depth, 1)
        self.assertEqual(category.parent_category_id, 0)
        self.assertTrue(category.display_yn)
        self.assertEqual(category.target_group, "FEMALE")
        self.assertEqual(category.category_type, "NONE")
        self.assertEqual(category.path, "1")

        # Brand 검증
        self.assertEqual(product_group.brand.id, 1)
        self.assertEqual(product_group.brand.brand_name, "BrandX")
        self.assertEqual(product_group.brand.brand_icon_image_url, "https://brandx.com/logo.png")
        self.assertTrue(product_group.brand.display_yn)

        # Price 검증
        self.assertEqual(product_group.price.regular_price, 100000)
        self.assertEqual(product_group.price.current_price, 50000)
        self.assertEqual(product_group.price.sale_price, 50000)
        self.assertEqual(product_group.price.direct_discount_price, 50000)
        self.assertEqual(product_group.price.direct_discount_rate, 50)
        self.assertEqual(product_group.price.discount_rate, 50)

        # Config 검증
        self.assertEqual(product_group.config.product_group_config.config_id, 1)
        self.assertEqual(product_group.config.product_group_config.product_group_id, 1)
        self.assertTrue(product_group.config.product_group_config.active_yn)
        self.assertEqual(len(product_group.config.product_group_name_configs), 1)
        self.assertEqual(product_group.config.product_group_name_configs[0].country_code, "US")
        self.assertEqual(product_group.config.product_group_name_configs[0].custom_name, "")

        # Products 검증
        products = product_group_processing_data.products
        self.assertEqual(len(products), 2)

        product_1 = next(p for p in products if p.product_id == 1)
        self.assertEqual(product_1.product_group_id, 1)
        self.assertEqual(product_1.quantity, 10)
        self.assertFalse(product_1.sold_out_yn)
        self.assertTrue(product_1.display_yn)
        self.assertEqual(len(product_1.options), 2)

        option_1 = next(o for o in product_1.options if o.option_name == "COLOR")
        self.assertEqual(option_1.option_value, "Black")

        # ExternalMallProductPendingData 검증
        external_data = product_group_processing_data.external_mall_product_pending_data[0]
        self.assertEqual(external_data.site_id, 1)
        self.assertEqual(external_data.product_group_id, 1)
        self.assertEqual(external_data.policy_id, 1)
        self.assertEqual(external_data.country_code, "US")
        self.assertTrue(external_data.translated_needed)


if __name__ == "__main__":
    unittest.main()
