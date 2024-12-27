from dataclasses import dataclass
from enum import Enum

@dataclass
class BatchDataTypeConfig:
    name: str
    max_tokens: int
    model: str
    description: str



class BatchDataType(Enum):
    TITLE = BatchDataTypeConfig(
        name="title",
        max_tokens=1500,
        model="gpt-4o-mini",
        description="상품 제목 생성"
    )

    TEST_CODE = BatchDataTypeConfig(
        name="test_code",
        max_tokens=4000,
        model="gpt-4",
        description="테스트 코드 생성"
    )

    def __str__(self):
        return self.value.name

    @property
    def max_tokens(self):
        return self.value.max_tokens

    @property
    def model(self):
        return self.value.model

    @property
    def description(self):
        return self.value.description