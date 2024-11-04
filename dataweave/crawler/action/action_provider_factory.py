from dataweave.crawler.action.action_provider import ActionProvider
from dataweave.crawler.action.save_s3_action_provider import SaveS3ActionProvider


class ActionProviderFactory:
    @staticmethod
    def get_action_provider(action_type: str) -> ActionProvider:
        if action_type == "SAVE_S3":
            return SaveS3ActionProvider()

        raise ValueError(f"Unsupported action type: {action_type}")