from typing import Type, TypeVar

T = TypeVar("T")


class ConfigDeserializer:
    def deserialize(self, value: str, type: Type[T]) -> T:
        if hasattr(type, "from_string"):
            return type.from_string(value)
        else:
            return type(value)
