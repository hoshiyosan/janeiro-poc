from janeiro.config.loader.base import ConfigLoader
from janeiro.config.options import ConfigOption
from janeiro.constants import UNDEFINED


class Configuration:
    def __init__(self, loader: ConfigLoader):
        self._loader = loader

    def get(self, option: ConfigOption):
        value = self._loader.get(option)
        if option.is_required() and value is UNDEFINED:
            raise ValueError(self._loader.get_missing_key_error_message(option.key))
        return value

    def get_option_name(self, key: str):
        return self._loader.get_option_name(key)
