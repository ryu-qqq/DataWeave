import json

from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse
from dataweave.gpt.prompt_generator import PromptGenerator


class OptionsPromptGenerator(PromptGenerator):
    def get_question(self, product: GptTrainingDataResponse) -> str:
        product_group_id = product.product_group.product_group_id
        brand_name = product.brand.brand_name
        categories = product.categories
        products = product.products

        options_as_dicts = [
            [option.to_dict() for option in product.options] for product in products
        ]

        return (
            f"다음 상품 옵션 데이터를 분석하고 아래 형식으로 반환하세요. 추가 설명은 포함하지 마세요:\n"
            f"1. 원본 옵션 리스트를 문자열로 반환하세요.\n"
            f"2. 카테고리 이름과 브랜드를 고려하여 옵션 값을 변환하세요:\n"
            f"   - 카테고리에 '신발'이 포함된 경우, 브랜드에 따라 옵션 값을 한국 발 사이즈(mm)로 변환하세요. "
            f"예: ['260mm', '270mm', '280mm'].\n"
            f"   - 카테고리에 '옷'이 포함된 경우, 브랜드에 따라 옵션 값을 'S', 'M', 'L' 등의 단어로 변환하세요.\n"
            f"3. 옵션 값이 범위(S-M, 240-250 등)로 주어진 경우, 범위 중 **큰 값**만 반환하세요.\n"
            f"4. 옵션 값이 OS, one-size 등 단일 옵션을 뜻하는 경우 FREE로 통일 해주세요.\n"
            f"5. 원본 옵션의 단위를 기록하세요 (예: 'US', 'UK').\n\n"
            f"반환 형식:\n"
            f"{{\n"
            f"    \"product_group_id\": <int>,\n"
            f"    \"brand_name\": <str>,\n"
            f"    \"original_options\": <list>,\n"
            f"    \"normalized_options\": {{\"sizes\": <list>, \"unit\": <str>}}\n"
            f"}}\n\n"
            f"입력 데이터:\n"
            f"상품그룹 아이디: {product_group_id}\n"
            f"브랜드: {brand_name}\n"
            f"카테고리: {categories}\n"
            f"상품 옵션:\n"
            f"{json.dumps(options_as_dicts, ensure_ascii=False, indent=2)}"
        )
