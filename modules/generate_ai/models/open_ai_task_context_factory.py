from injector import singleton, Injector

from modules.generate_ai.models.open_ai_enums import GenerativeAiType, PerformerType
from modules.generate_ai.models.open_ai_task_context import OpenAiTaskContext
from modules.generate_ai.models.task_context import TaskContext
from modules.generate_ai.models.task_context_factory import TaskContextFactory


@singleton
class OpenAiTaskContextFactory(TaskContextFactory):

    def supports(self, ai_type: GenerativeAiType) -> bool:
        return ai_type == GenerativeAiType.OPENAI

    def create_context(self, system_message: str, user_message: str, **kwrgs) -> TaskContext:
        model = kwrgs.get("model", "gpt-4o")
        temperature = kwrgs.get("temperature", 0.7)
        is_realtime = kwrgs.get("is_realtime", True)
        perform_type = kwrgs.get("perform_type", PerformerType.REVIEWER)

        return OpenAiTaskContext(
            system_message=system_message,
            user_message=user_message,
            model=model,
            temperature=temperature,
            is_realtime=is_realtime,
            perform_type=perform_type
        )


injector = Injector()
open_ai_task_context_factory = injector.get(OpenAiTaskContextFactory)
