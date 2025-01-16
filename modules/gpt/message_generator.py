import asyncio
import logging
from typing import List, Any

from injector import singleton, inject

from modules.gpt.models.product_data_type import BatchDataType
from modules.gpt.models.prompt_models import Prompt
from modules.gpt.prompt_generator import PromptGenerator
from modules.gpt.prompt_generator_strategy_factory import PromptGeneratorFactory


@singleton
class MessageGenerator:

    @inject
    def __init__(self, question_provider_factory: PromptGeneratorFactory):
        self.__question_provider_factory = question_provider_factory

    async def generate_messages(self, items: List[Any], data_type: BatchDataType) -> List[Prompt]:

        try:
            provider = self.__question_provider_factory.get_provider(data_type)
            prompts = await self.__generate_prompts(provider, items)

            return prompts
        except Exception as e:
            logging.error(f"Error generating messages for {data_type.value}: {e}")
            raise

    async def __generate_prompts(self, provider: PromptGenerator, items: List[Any]) -> List[Prompt]:
        prompts = await asyncio.gather(*(provider.get_prompt(item) for item in items))
        return [prompt for sublist in prompts for prompt in sublist]
