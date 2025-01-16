import json
import logging
import os
import uuid
from datetime import datetime
from typing import List, Any

import aiofiles
from injector import singleton, inject

from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.message_generator import MessageGenerator
from modules.gpt.models.batch_models import BatchFile
from modules.gpt.models.prompt_models import Prompt


@singleton
class BatchFileCreator:

    @inject
    def __init__(self, message_generator: MessageGenerator):
        self.__message_generator = message_generator
        self.__base_dir = os.path.join(os.getcwd(), "batch", "processing")
        os.makedirs(self.__base_dir, exist_ok=True)

    async def create_batch_files(self, items: List[Any], data_type: BatchDataType) -> List[BatchFile]:

        try:
            prompts = await self.__message_generator.generate_messages(items, data_type)

            batch_files = [await self.__create_single_batch_file(prompt, data_type) for prompt in prompts]
            logging.info(f"Created {len(batch_files)} batch files for {data_type.value}")

            return batch_files
        except Exception as e:
            logging.error(f"Error creating batch files: {e}")
            raise

    async def __create_single_batch_file(self, prompt: Prompt, data_type: BatchDataType) -> BatchFile:

        file_path = self.__generate_file_path(data_type)

        try:
            async with aiofiles.open(file_path, "w") as f:
                batch_item = prompt.to_task(
                    model=data_type.model,
                    temperature=data_type.temperature,
                    custom_id_prefix=data_type.value,
                )
                await f.write(json.dumps(batch_item) + "\n")

            return BatchFile(
                id=prompt.metadata.get_id(),
                file_path=file_path,
                metadata=prompt.metadata,
            )

        except Exception as e:
            logging.error(f"Error writing to file {file_path}: {e}")
            raise

    def __generate_file_path(self, data_type: BatchDataType) -> str:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = uuid.uuid4().hex[:8]
        return os.path.join(self.__base_dir, f"batch_{data_type.name}_{timestamp}_{random_id}.jsonl")