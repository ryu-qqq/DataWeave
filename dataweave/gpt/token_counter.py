from typing import List

import tiktoken

from dataweave.gpt.prompt import Prompt


class TokenCounter:
    @staticmethod
    def count_tokens(messages: list[dict], model: str = "gpt-4o") -> int:
        encoding = tiktoken.encoding_for_model(model)
        total_tokens = 0

        for message in messages:
            total_tokens += len(encoding.encode(message["role"]))
            total_tokens += len(encoding.encode(message["content"]))
        return total_tokens

    @staticmethod
    def chunkify_by_token_limit(data: List[Prompt], model: str, max_tokens: int) -> List[List[Prompt]]:
        encoding = tiktoken.encoding_for_model(model)
        chunks = []
        current_chunk = []
        current_tokens = 0

        for prompt in data:
            messages = prompt.to_message_list()
            message_tokens = TokenCounter.count_tokens(messages, model)

            if current_tokens + message_tokens > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_tokens = 0

            current_chunk.append(prompt)
            current_tokens += message_tokens

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
