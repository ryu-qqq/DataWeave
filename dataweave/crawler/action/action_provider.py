from dataweave.cache.redis_cache_manager import redis_cache_manager
from dataweave.crawler.action.action_interface import ActionInterface
from dataweave.crawler.action.api_call_actor import api_call_actor
from dataweave.crawler.action.save_cache_actor import SaveCacheActor
from dataweave.crawler.action.save_s3_actor import save_s3_actor
from dataweave.enums.action_type import Action


class ActionProvider:

    @staticmethod
    def get_action_provider(action_type: str) -> ActionInterface:
        if action_type == Action.SAVE_S3.name:
            return save_s3_actor
        elif action_type == Action.SAVE_CACHE.name:
            return SaveCacheActor(redis_cache_manager)
        elif action_type == Action.API_CALL.name:
            return api_call_actor

        raise ValueError(f"Unsupported action type: {action_type}")