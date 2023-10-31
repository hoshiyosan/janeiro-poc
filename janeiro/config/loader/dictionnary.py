from janeiro.config.loader.base import ConfigLoader


class DictionnaryConfigLoader(ConfigLoader):
    def get_option_name(self, key: str):
        return key
