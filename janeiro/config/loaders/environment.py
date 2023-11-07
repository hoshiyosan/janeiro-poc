import os

from janeiro.config.loaders import ConfigLoader
from janeiro.exc import ConfigurationError
from janeiro.types import UNDEFINED


class EnvironmentConfigLoader(ConfigLoader):
    def __init__(self, prefix: str = None):
        self.prefix = prefix

    def _get_variable_name(self, key: str):
        prefixed_key = key if self.prefix is None else self.prefix + "." + key
        return prefixed_key.replace(".", "_").upper()

    def get(self, key):
        variable_name = self._get_variable_name(key)
        return os.getenv(variable_name, UNDEFINED)

    def raise_missing_key(self, key: str):
        variable_name = self._get_variable_name(key)
        raise ConfigurationError("Missing environment variable: %s" % variable_name)
