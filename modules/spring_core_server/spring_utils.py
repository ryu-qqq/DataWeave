from enum import Enum
from typing import Dict, Any


class StringUtils:
    @staticmethod
    def convert_to_camel_case(snake_case_dict: Dict[str, Any]) -> Dict[str, str]:
        """
        Convert a dictionary's keys from snake_case to camelCase and process Enum values.

        :param snake_case_dict: Dictionary with snake_case keys.
        :return: Dictionary with camelCase keys.
        """
        camel_case_dict = {}
        for key, value in snake_case_dict.items():
            camel_case_key = StringUtils.to_camel_case(key)
            camel_case_dict[camel_case_key] = StringUtils.query_var(value)  # Enum 처리 추가
        return camel_case_dict

    @staticmethod
    def to_camel_case(snake_str: str) -> str:
        """
        Convert a snake_case string to camelCase.

        :param snake_str: String in snake_case format.
        :return: String in camelCase format.
        """
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def serialize_and_convert_to_camel_case(data_model: Any) -> Dict[str, Any]:
        """
        Serialize a data model and convert its keys to camelCase.

        :param data_model: Data model object with a to_dict() method.
        :return: Serialized dictionary with camelCase keys.
        """
        serialized_data = data_model.to_dict()
        return StringUtils.convert_to_camel_case(serialized_data)

    @staticmethod
    def query_var(value: Any) -> str:
        """
        Convert values to a string format suitable for query parameters.
        Handles enums and other primitive types.

        :param value: The value to convert.
        :return: The value as a string.
        """
        if isinstance(value, Enum):  # Enum 처리
            return value.name  # Enum의 name 속성 사용
        return str(value)
