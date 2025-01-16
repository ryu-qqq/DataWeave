from abc import ABC, abstractmethod

from modules.generate_ai.models.open_ai_enums import GenerativeAiType
from modules.generate_ai.models.task_context import TaskContext


class TaskContextFactory(ABC):

    @abstractmethod
    def supports(self, ai_type: GenerativeAiType) -> bool:
        pass

    @abstractmethod
    def create_context(self, system_message: str, user_message: str, **kwrgs) -> TaskContext:
        """
                Creates a TaskContext for the given parameters.

                :param system_message: The system message for the AI model.
                :param user_message: The user message for the AI model.
                :param kwrgs: Additional optional parameters for context creation.
                              Examples:
                              - model: The AI model name (e.g., "gpt-4").
                              - temperature: Sampling temperature for the model.
                              - is_realtime: Boolean indicating real-time execution.
                :return: An instance of TaskContext.
                """
        pass



