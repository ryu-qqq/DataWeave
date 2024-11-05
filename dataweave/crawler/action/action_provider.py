from dataweave.crawler.action.action_interface import ActionInterface
from dataweave.crawler.action.save_s3_action_provider import save_s3_action_provider
from dataweave.enums.action_type import ActionType


class ActionProvider:

    @staticmethod
    def get_action_provider(action_type: str) -> ActionInterface:
        if action_type == ActionType.SAVE_S3.name:
            return save_s3_action_provider

        raise ValueError(f"Unsupported action type: {action_type}")