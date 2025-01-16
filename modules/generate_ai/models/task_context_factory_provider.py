from typing import List, Optional

from modules.generate_ai.models.open_ai_enums import GenerativeAiType
from modules.generate_ai.models.open_ai_task_context_factory import open_ai_task_context_factory
from modules.generate_ai.models.task_context_factory import TaskContextFactory


class TaskContextFactoryProvider:

    def __init__(self, factories: List[TaskContextFactory]):
        self.factories = factories

    def get_factory(self, ai_type: GenerativeAiType) -> Optional[TaskContextFactory]:

        for factory in self.factories:
            if factory.supports(ai_type):
                return factory
        return None


task_context_provider = TaskContextFactoryProvider(factories=[open_ai_task_context_factory])