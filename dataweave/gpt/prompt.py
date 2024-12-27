from typing import List, Optional, Dict, Any


class Prompt:
    def __init__(self, system_message: str, user_message: str, metadata: Optional[Dict[str, Any]] = None):
        self.system_message = system_message
        self.user_message = user_message
        self.metadata = metadata or {}

    def to_message_list(self) -> List[dict]:
        return [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": self.user_message}
        ]