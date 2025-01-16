import logging
from typing import Optional

from modules.generate_ai.executor.executor import Executor
from modules.generate_ai.models.task_context import TaskContext


class ExecutorProvider:

    def __init__(self, executors: list[Executor]):
        self.executors = executors

    def get_executor(self, context: TaskContext) -> Optional[Executor]:
        for executor in self.executors:
            if executor.supports(context):
                return executor

        logging.warning(f"No executor found for context: {context}")
        return None


executor_provider = ExecutorProvider(executors=[review_report_generator, test_code_report_generator])