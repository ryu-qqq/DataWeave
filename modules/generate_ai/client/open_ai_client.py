from abc import ABC, abstractmethod


class OpenAiClient(ABC):
    """
    Abstract base class for OpenAI client interactions.
    Defines the common interface for both batch and real-time operations.
    """

    @abstractmethod
    def generate_prompt(self, system_message: str, user_message: str, model: str, temperature: float) -> str:
        """
        Generate a response based on the provided system and user messages.

        :param system_message: Context or instructions for the AI.
        :param user_message: User's input message.
        :param model: OpenAI model to use (e.g., "gpt-4").
        :param temperature: Sampling temperature.
        :return: AI-generated response.
        """
        pass