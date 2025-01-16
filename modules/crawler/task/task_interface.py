from abc import ABC, abstractmethod


class TaskInterface(ABC):

    @abstractmethod
    async def processing(self, **kwargs):
        pass
