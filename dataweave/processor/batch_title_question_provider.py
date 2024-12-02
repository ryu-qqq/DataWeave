import json

from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse
from dataweave.processor.question_provider import QuestionProvider


class TitleQuestionProvider(QuestionProvider):
    def get_question(self, product: GptTrainingDataResponse) -> str:
        return (
            f"다음 상품 제목 데이터를 분석하고 아래 형식으로 반환하세요. 추가 설명은 포함하지 마세요:\n"
            f"1. 제목에서 브랜드명, 색상, 스타일 코드를 추출하세요.\n"
            f"2. 상품과 관련있는 단어만 남기고 불필요한 단어(판매자 이름을 뜻하는 단어 및 '즉시', '당일' 등) 상품과 관련없는 단어를 삭제하세요.\n"
            f"3. 상품명은 국가 코드별로 번역된 결과를 포함하세요.\n"
            f"4. 상품명에 브랜드명, 색상, 스타일 코드개 있으면 영어로 변환해 그대로 유지하세요.\n\n"
            f"5. 단 상품명이 60자를 넘어간다면 60자 이내로 줄여주세요.\n\n"
            f"반환 형식:\n"
            f"{{\n"
            f"    \"product_group_id\": <int>,\n"
            f"    \"original_title\": <str>,\n"
            f"    \"filtered_title\": {{\"KR\": <str>, \"US\": <str>}},\n"
            f"    \"brand_name\": <str>,\n"
            f"    \"style_code\": <str>,\n"
            f"    \"color_in_title\": <str>,\n"
            f"    \"deleted_words\": <list>\n"
            f"}}\n\n"
            f"입력 데이터:\n"
            f"상품그룹 아이디:{product.product_group.product_group_id}\n"
            f"{json.dumps(product.product_group.product_group_name, ensure_ascii=False)}"
        )