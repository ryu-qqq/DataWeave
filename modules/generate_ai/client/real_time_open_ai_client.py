import logging

from injector import singleton, inject, Injector
from openai import Client

from modules.generate_ai.client.open_ai_client import OpenAiClient
from modules.generate_ai.openai_config import OpenAiConfig


@singleton
class RealTimeOpenAIClient(OpenAiClient):

    @inject
    def __init__(self, config: OpenAiConfig):
        self.client = Client(api_key=config.API_KEY)

    def generate_prompt(self, system_message: str, user_message: str, model: str, temperature: float) -> str:

        try:
            logging.info("Generating prompt using OpenAI API...")
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
            )
            choices = response.choices
            if not choices:
                raise ValueError("No choices found in response.")

            prompt = choices[0].message.content
            logging.info("Prompt generated successfully.")
            return prompt
        except Exception as e:
            logging.error(f"Error generating prompt: {e}")
            raise


injector = Injector()
real_time_open_api_client = injector.get(RealTimeOpenAIClient)