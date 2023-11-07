from dataclasses import dataclass
from typing import Callable, Generic, Type, TypeVar

from janeiro.types import UNDEFINED

T = TypeVar("T")


@dataclass
class ConfigOption(Generic[T]):
    key: str
    type: Type[T]
    default: Type[T] = UNDEFINED
    default_factory: Callable[[], Type[T]] = UNDEFINED

    def get_default(self) -> T:
        if self.default_factory != UNDEFINED:
            default_value = self.default_factory()
        elif self.default != UNDEFINED:
            default_value = self.default
        else:
            default_value = UNDEFINED

        return default_value
