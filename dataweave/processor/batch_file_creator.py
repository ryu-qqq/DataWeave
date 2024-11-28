import json
import logging
import os
import uuid
from datetime import datetime
from typing import List

from injector import singleton

from dataweave.api_client.models.product_group_context_response import ProductGroupProcessingDataResponse, \
    GptTrainingDataResponse
from dataweave.enums.product_data_type import ProductDataType
from dataweave.processor.question_provider_factory import QuestionProviderFactory
from dataweave.processor.token_counter import TokenCounter


@singleton
class BatchFileCreator:

    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), "batch", "processing")
        os.makedirs(self.base_dir, exist_ok=True)

    def create_batch_file(self, data: List[ProductGroupProcessingDataResponse], data_type: ProductDataType) -> str:
        try:

            file_path = self.generate_file_path(data_type)
            total_tokens = 0

            with open(file_path, "w") as f:
                for item in data:
                    messages = self.create_message(item, data_type)
                    batch_item = {
                        "custom_id": f"product-{item.product_group.product_group_id}-{data_type.value}",
                        "method": "POST",
                        "url": "/v1/chat/completions",
                        "body": {
                            "model": "gpt-4o-mini",
                            "messages": messages,
                            "max_tokens": 1500
                        }
                    }
                    f.write(json.dumps(batch_item) + "\n")
                    total_tokens += TokenCounter.count_tokens(messages)

            logging.info(f"Batch file created successfully for {data_type.value}: {file_path}")
            logging.info(f"Total tokens for {data_type.value}: {total_tokens}")

            return file_path

        except Exception as e:
            logging.info(f"Error creating batch file: {e}")
            raise

    def create_message(self, item: GptTrainingDataResponse, data_type: ProductDataType) -> List[dict]:

        provider = QuestionProviderFactory.get_provider(data_type)
        user_content = provider.get_question(item)

        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_content}
        ]

    def generate_file_path(self, data_type: ProductDataType) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = uuid.uuid4().hex[:8]
        return os.path.join(self.base_dir, f"batch_{data_type}_{timestamp}_{random_id}.jsonl")