from typing import Dict

from janeiro.config.loader.base import ConfigLoader


class DictionnaryConfigLoader(ConfigLoader):
    def __init__(self, config: Dict[str, str]):
        self.config = config

    def get_option_name(self, key: str):
        return key

    def get(self, key: str):
        option_name = self.get_option_name(key)
        return self.config.get(option_name)
