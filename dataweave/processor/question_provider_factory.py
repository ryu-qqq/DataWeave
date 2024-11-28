from dataweave.enums.product_data_type import ProductDataType
from dataweave.processor.batch_description_question import DescriptionQuestionProvider
from dataweave.processor.batch_option_questino_provider import OptionsQuestionProvider
from dataweave.processor.batch_title_question_provider import TitleQuestionProvider
from dataweave.processor.question_provider import QuestionProvider


class QuestionProviderFactory:
    @staticmethod
    def get_provider(data_type: ProductDataType) -> QuestionProvider:
        if data_type == ProductDataType.TITLE:
            return TitleQuestionProvider()
        # elif data_type == ProductDataType.DESCRIPTION:
        #     return DescriptionQuestionProvider()
        # elif data_type == ProductDataType.OPTIONS:
        #     return OptionsQuestionProvider()
        else:
            raise ValueError(f"지원되지 않는 데이터 타입: {data_type}")
