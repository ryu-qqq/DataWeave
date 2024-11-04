from abc import abstractmethod, ABC
from typing import Dict, Any


class ActionProvider(ABC):
    @abstractmethod
    def perform_action(self, data: Any):
        pass
