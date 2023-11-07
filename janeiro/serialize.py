from abc import ABC, abstractmethod
from typing import Type, TypeVar

T = TypeVar("T")


class Deserializer(ABC):
    @abstractmethod
    def deserialize(self, raw_value: str, type: Type[T]) -> T:
        raise NotImplementedError


class DefaultDeserializer(Deserializer):
    def deserialize(self, raw_value, type):
        if isinstance(raw_value, type):
            return raw_value
        else:
            return type(raw_value)
