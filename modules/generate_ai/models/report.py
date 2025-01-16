from abc import ABC, abstractmethod


class Report(ABC):

    @abstractmethod
    def to_string(self) -> str:
        pass

