from logging import getLogger

from janeiro.config.cache import ConfigCache
from janeiro.config.deserializer import ConfigDeserializer
from janeiro.config.loader.base import ConfigLoader
from janeiro.config.options import ConfigOption
from janeiro.constants import UNDEFINED

LOG = getLogger("janeiro.config")


class Configuration:
    def __init__(self, loader: ConfigLoader, deserializer: ConfigDeserializer = None):
        self._cache = ConfigCache()
        self._set_config_loader(loader)
        self._set_config_deserializer(deserializer)

    def _set_config_loader(self, loader: ConfigLoader):
        if not isinstance(loader, ConfigLoader):
            raise TypeError("Loader must extend base class ConfigLoader")
        self._loader = loader

    def _set_config_deserializer(self, deserializer: ConfigDeserializer):
        if deserializer is None:
            deserializer = ConfigDeserializer()
        if not isinstance(deserializer, ConfigDeserializer):
            raise TypeError("Deserializer must extend base class ConfigDeserializer")
        self._deserializer = deserializer

    def get(self, option: ConfigOption):
        value = self._cache.get(option)
        if value != UNDEFINED:
            LOG.info("Cache hit getting config option %s: %s", option.key, value)
            return value

        value = self._loader.get(option.key)
        if option.is_required() and value is UNDEFINED:
            raise ValueError(self._loader.get_missing_key_error_message(option.key))

        if not isinstance(value, option.type) and isinstance(value, str):
            value = self._deserializer.deserialize(value, option.type)

        if not isinstance(value, option.type):
            raise TypeError(
                "Wrong value type for config option %s. Expected %s, got value: %s"
                % (option.key, option.type, value)
            )

        LOG.debug("Config option loaded %s=%s", option.key, value)
        self._cache.set(option, value)

        return value

    def get_cache(self):
        return self._cache.value()

    def get_option_name(self, key: str):
        return self._loader.get_option_name(key)
