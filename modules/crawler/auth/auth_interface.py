from abc import abstractmethod, ABC
from typing import Dict


class AuthInterface(ABC):
    @abstractmethod
    async def authenticate(self, auth_endpoint: str, headers: Dict[str, str], auth_header: str, payload: str) -> Dict[str, str]:
        pass
