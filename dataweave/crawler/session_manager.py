from abc import ABC, abstractmethod


class SessionManager(ABC):
    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def close_session(self):
        pass
