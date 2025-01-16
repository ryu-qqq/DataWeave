from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from modules.generate_ai.models.report import Report
from modules.generate_ai.models.task_context import TaskContext

T = TypeVar("T", bound=TaskContext)
R = TypeVar("R", bound=Report)


class Executor(ABC, Generic[T, R]):

    @abstractmethod
    def supports(self, context: T) -> bool:
        pass

    @abstractmethod
    def execute(self, context: T) -> R:
        pass
