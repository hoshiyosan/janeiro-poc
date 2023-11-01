from typing import Any, Iterable, Tuple, TypeVar, Union

from janeiro.config.options import ConfigOption
from janeiro.constants import UNDEFINED

T = TypeVar("T")


class ConfigCache:
    def __init__(self):
        self.registry = {}

    def value(self):
        return {key: self.registry[key] for key in self.registry}

    def set(self, option: ConfigOption[T], value: T):
        self.registry[option.key] = value

    def get(self, option: ConfigOption[T]) -> Union[T, UNDEFINED]:
        return self.registry.get(option.key, UNDEFINED)
