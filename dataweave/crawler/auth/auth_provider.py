from abc import abstractmethod, ABC
from typing import Dict, Any


class AuthProvider(ABC):
    @abstractmethod
    def authenticate(self, auth_endpoint: str, headers: Dict[str, str], auth_header: str, payload: str) -> Dict[str, str]:
        pass
