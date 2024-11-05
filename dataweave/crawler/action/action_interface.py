from abc import abstractmethod, ABC


class ActionInterface(ABC):
    @abstractmethod
    def action(self, **kwargs):
        pass
