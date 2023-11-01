import os

from janeiro.config.loader.base import ConfigLoader
from janeiro.config.options import ConfigOption
from janeiro.constants import UNDEFINED


class EnvironmentConfigLoader(ConfigLoader):
    def __init__(self, prefix: str = None):
        self.prefix = prefix

    def get_option_name(self, key: str):
        return (
            (self.prefix + "." + key if self.prefix else key).replace(".", "_").upper()
        )

    def get_missing_key_error_message(self, key: str):
        return "Missing required environment variable: %s" % self.get_option_name(key)

    def get(self, key: str):
        variable_name = self.get_option_name(key)
        return os.getenv(variable_name, UNDEFINED)
