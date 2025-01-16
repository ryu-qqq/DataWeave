from dataclasses import dataclass
from enum import Enum


@dataclass
class BatchDataTypeConfig:
    name: str
    max_tokens: int
    model: str
    description: str
    temperature: float


class BatchDataType(Enum):
    PRODUCT = BatchDataTypeConfig(
        name="PRODUCT",
        max_tokens=1500,
        model="gpt-4o",
        description="Product Info",
        temperature=0.1
    )

    TEST_CODE = BatchDataTypeConfig(
        name="TEST_CODE",
        max_tokens=4000,
        model="gpt-4o",
        description="Test Code Generate",
        temperature=0.1
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

    @property
    def temperature(self):
        return self.value.temperature
