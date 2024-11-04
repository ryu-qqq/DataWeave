from typing import Any

from dataweave.crawler.action.action_provider import ActionProvider


class SaveS3ActionProvider(ActionProvider):
    def perform_action(self, data: Any):
        print(f"Data saved to S3: {data}")