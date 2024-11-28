from typing import List, Any

import tiktoken

from dataweave.enums.product_data_type import ProductDataType


class TokenCounter:
    @staticmethod
    def count_tokens(messages: list[dict], model: str = "gpt-3.5-turbo") -> int:
        encoding = tiktoken.encoding_for_model(model)
        total_tokens = 0

        for message in messages:
            total_tokens += len(encoding.encode(message["role"]))
            total_tokens += len(encoding.encode(message["content"]))
        return total_tokens

    @staticmethod
    def chunkify_by_token_limit(data: List[Any], model: str, max_tokens: int, message_generator,
                                data_type: ProductDataType) -> List[List[Any]]:
        """
        주어진 데이터 리스트를 OpenAI 모델의 토큰 제한에 맞게 청크화, 데이터 타입별로 처리.
        :param data: 데이터 리스트
        :param model: OpenAI 모델 이름 (예: 'gpt-3.5-turbo')
        :param max_tokens: 최대 허용 토큰 수
        :param message_generator: 메시지를 생성하는 함수
        :param data_type: 처리 중인 데이터 타입
        :return: 데이터 타입별로 청크화된 리스트
        """
        encoding = tiktoken.encoding_for_model(model)
        chunks = []
        current_chunk = []
        current_tokens = 0

        for item in data:
            messages = message_generator(item, data_type)
            message_tokens = TokenCounter.count_tokens(messages, model)

            if current_tokens + message_tokens > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_tokens = 0

            current_chunk.append(item)
            current_tokens += message_tokens

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
