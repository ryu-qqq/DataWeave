from abc import ABC, abstractmethod
from typing import Any, Optional


class ResponseParser(ABC):
    @abstractmethod
    def parse(self, response: Any) -> Optional[Any]:
        pass
