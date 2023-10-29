from dataclasses import dataclass
import os
from typing import Generic, List, Type, TypeVar

T = TypeVar("T")


@dataclass
class ConfigOption(Generic[T]):
    key: str
    description: str
    type: Type[T]


class ConfigLoader:
    def get_option_name(self, key: str) -> str:
        raise NotImplementedError


class EnvironmentConfigLoader(ConfigLoader):
    def __init__(self, prefix: str = None):
        self.prefix = prefix

    def get_option_name(self, key: str):
        return (
            (self.prefix + "." + key if self.prefix else key).replace(".", "_").upper()
        )

    def get(self, option: ConfigOption):
        variable_name = self.get_option_name(option.key)
        return os.getenv(variable_name)


def package_relative_path(path: str):
    import os, inspect
    parent_folder = os.path.dirname(inspect.stack()[1].filename)
    absolute_path = os.path.join(parent_folder, path)
    print(absolute_path)
    return absolute_path


class DictConfigLoader(ConfigLoader):
    def get_option_name(self, key: str):
        return key


class Configuration:
    def __init__(self, loader: ConfigLoader):
        self._loader = loader

    def get(self, key: str):
        return self._loader.get(key)

    def get_option_name(self, key: str):
        return self._loader.get_option_name(key)


REGISTERED_OPTIONS: List[ConfigOption] = []


def register_options(*options: ConfigOption):
    REGISTERED_OPTIONS.extend(options)


def print_options(config: Configuration):
    sorted_options = sorted(REGISTERED_OPTIONS, key=lambda option: option.key)

    option_name_max_length = 0
    for option in sorted_options:
        option_name_length = len(config.get_option_name(option.key))
        if option_name_length > option_name_max_length:
            option_name_max_length = option_name_length

    for option in sorted_options:
        print(
            config.get_option_name(option.key).ljust(option_name_max_length + 3),
            option.description
            if isinstance(option.description, str)
            else option.description[0],
        )
        if isinstance(option.description, tuple):
            for row in option.description[1:]:
                print(" " * (option_name_max_length + 3), row)
        print()
