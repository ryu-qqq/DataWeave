import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from typing import List, Any, Tuple, Dict

import aiofiles
from injector import singleton, inject

from dataweave.enums.product_data_type import BatchDataType
from dataweave.gpt.prompt import Prompt
from dataweave.gpt.prompt_generator_strategy_factory import PromptGeneratorFactory
from dataweave.gpt.token_counter import TokenCounter


@singleton
class BatchFileCreator:

    @inject
    def __init__(self, question_provider_factory: PromptGeneratorFactory):
        self.question_provider_factory = question_provider_factory
        self.base_dir = os.path.join(os.getcwd(), "batch", "processing")
        os.makedirs(self.base_dir, exist_ok=True)

    async def create_batch_files(self, prompts: List[Prompt], data_type: BatchDataType) -> Tuple[str, Dict[str, Any]]:
        return await self._create_batch_file_internal(prompts, data_type)

    async def create_batch_file(self, prompt: Prompt, data_type: BatchDataType) -> Tuple[str, Dict[str, Any]]:
        return await self._create_batch_file_internal([prompt], data_type)

    async def create_messages(self, items: List[Any], data_type: BatchDataType) -> List[Prompt]:
        provider = self.question_provider_factory.get_provider(data_type)
        all_prompts = await asyncio.gather(*(provider.get_prompt(item) for item in items))

        flattened_prompts = [prompt for sublist in all_prompts for prompt in sublist]

        return flattened_prompts

    def generate_file_path(self, data_type: BatchDataType) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = uuid.uuid4().hex[:8]
        return os.path.join(self.base_dir, f"batch_{data_type.value}_{timestamp}_{random_id}.jsonl")

    async def _create_batch_file_internal(self, prompts: List[Prompt], data_type: BatchDataType) -> Tuple[str, Dict[str, Any]]:
        try:
            file_path = self.generate_file_path(data_type)
            total_tokens = 0
            metadata = {}

            async with aiofiles.open(file_path, "w") as f:
                for prompt in prompts:
                    messages = prompt.to_message_list()
                    metadata.update(prompt.metadata)

                    batch_item = self._create_batch_item(messages, data_type)
                    await f.write(json.dumps(batch_item) + "\n")

                    total_tokens += TokenCounter.count_tokens(messages)

            logging.info(f"Batch file created successfully for {data_type.value}: {file_path}")
            logging.info(f"Total tokens for {data_type.value}: {total_tokens}")

            return file_path, metadata

        except Exception as e:
            logging.error(f"Error creating batch file: {e}")
            raise

    def _create_batch_item(self, messages: List[dict], data_type: BatchDataType) -> dict:
        return {
            "custom_id": f"{data_type.value}-{uuid.uuid4().hex[:8]}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": data_type.model,
                "messages": messages,
                "max_tokens": data_type.max_tokens,
            },
        }
