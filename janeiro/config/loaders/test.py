from typing import Dict

from janeiro.config.loaders import ConfigLoader
from janeiro.exc import ConfigurationError


class TestConfigLoader(ConfigLoader):
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def get(self, key: str):
        return self.config.get(key)

    def raise_missing_key(self, key: str):
        raise ConfigurationError("Missing configuration key: %s" % key)
