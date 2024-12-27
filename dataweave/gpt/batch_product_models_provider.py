from dataweave.enums.product_data_type import BatchDataType
from dataweave.gpt.batch_product_models import BatchProductModel, TitleResponse, OptionsResponse, \
    DescriptionResponse


class BatchProductProvider:
    @staticmethod
    def from_json(data_type: BatchDataType, data: dict) -> BatchProductModel:
        if data_type == BatchDataType.TITLE.name:
            return TitleResponse.from_json(data)
        # elif data_type == BatchDataType.OPTIONS.name:
        #     return OptionsResponse.from_json(data)
        # elif data_type == BatchDataType.DESCRIPTION.name:
        #     return DescriptionResponse.from_json(data)

        else:
            raise ValueError(f"Unsupported data type: {data_type}")