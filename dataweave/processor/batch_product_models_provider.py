from dataweave.enums.product_data_type import ProductDataType
from dataweave.processor.batch_product_models import BatchProductModel, TitleResponse, OptionsResponse, \
    DescriptionResponse


class BatchProductProvider:
    @staticmethod
    def from_json(data_type: ProductDataType, data: dict) -> BatchProductModel:
        if data_type == ProductDataType.TITLE.name:
            return TitleResponse.from_json(data)
        elif data_type == ProductDataType.OPTIONS.name:
            return OptionsResponse.from_json(data)
        elif data_type == ProductDataType.DESCRIPTION.name:
            return DescriptionResponse.from_json(data)

        else:
            raise ValueError(f"Unsupported data type: {data_type}")