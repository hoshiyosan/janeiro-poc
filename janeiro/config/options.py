from dataclasses import dataclass
from typing import Generic, Type, TypeVar

T = TypeVar("T")


@dataclass
class ConfigOption(Generic[T]):
    key: str
    description: str
    type: Type[T]

    def is_required(self):
        return False
