from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse
from dataweave.gpt.prompt_generator import PromptGenerator


class DescriptionPromptGenerator(PromptGenerator):
    def get_question(self, product: GptTrainingDataResponse) -> str:
        brand = product.brand
        categories = product.categories
        notice = product.product_group.product_notice
        product_name = product.product_group.product_group_name  # 상품 이름
        category_names = [category.category_name for category in categories]

        return (
            f"다음 상품 데이터를 기반으로 간결하고 매력적인 상품 설명을 만들어 주세요. "
            f"설명에는 상품의 브랜드, 카테고리, 소재, 색상, 사이즈 및 기타 관련 세부 정보가 포함되어야 합니다. "
            f"설명은 전문적이고 전자상거래 플랫폼에 적합한 톤으로 작성해 주세요. "
            f"불필요한 반복이나 여분의 텍스트를 피하세요.\n\n"
            f"입력 데이터의 필드 이름과 내용은 모두 영어로 변환되어야 합니다. "
            f"예를 들어, '카테고리'는 'Category'로 변환되어야 합니다.\n\n"
            f"브랜드 정보:\n"
            f" - 브랜드명(영어): {brand.brand_name}\n"
            f"카테고리 정보:\n"
            f" - 카테고리: {', '.join(category_names)}\n\n"
            f"상품 상세 정보:\n"
            f" - 상품명: {product_name}\n"
            f" - 소재: {notice.material if notice.material else 'N/A'}\n"
            f" - 색상: {notice.color if notice.color else 'N/A'}\n"
            f" - 사이즈: {notice.size if notice.size else 'N/A'}\n"
            f" - 세탁 방법: {notice.washing_method if notice.washing_method else 'N/A'}\n"
            f" - 제조 연월: {notice.year_month if notice.year_month else 'N/A'}\n"
            f" - 보증 기준: {notice.assurance_standard if notice.assurance_standard else 'N/A'}\n"
            f" - A/S 전화번호: {notice.as_phone if notice.as_phone else 'N/A'}\n\n"
            f"반환 형식:\n"
            f"{{\n"
            f"    \"product_group_id\": <int>,\n"
            f"    \"description\": <str>\n"
            f"}}\n\n"
            f"예시 형식:\n"
            f"{{\n"
            f"    \"product_group_id\": {product.product_group.product_group_id},\n"
            f"    \"description\": \"The {product_name} by {brand.brand_name} is crafted from {notice.material}. "
            f"This {', '.join(category_names)} product is available in {notice.color} and {notice.size}, "
            f"designed for excellence. It meets the highest standards of quality. For inquiries, contact {notice.as_phone}.\"\n"
            f"}}\n\n"
            f"위와 비슷한 JSON 객체를 입력 데이터에 맞춰 작성해 주세요. "
            f"입력 데이터의 모든 필드는 영어로 변환되어야 합니다."
        )