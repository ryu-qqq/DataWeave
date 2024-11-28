from abc import ABC, abstractmethod

from dataweave.api_client.models.product_group_context_response import GptTrainingDataResponse


class QuestionProvider(ABC):
    @abstractmethod
    def get_question(self, product: GptTrainingDataResponse) -> str:
        pass
