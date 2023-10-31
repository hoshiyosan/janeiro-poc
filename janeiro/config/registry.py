from typing import List

from janeiro.config.config import Configuration
from janeiro.config.options import ConfigOption

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
