import logging
from typing import Type, TypeVar

from janeiro.config.loaders import ConfigLoader
from janeiro.config.options import ConfigOption
from janeiro.exc import ConfigurationError
from janeiro.serialize import DefaultDeserializer, Deserializer
from janeiro.types import UNDEFINED

T = TypeVar("T")


class Configuration:
    def __init__(
        self,
        *,
        app_name: str,
        asgi_factory: str = None,
        loader: ConfigLoader,
        deserializer: Deserializer = None,
    ):
        self.app_name = app_name
        self.asgi_factory = asgi_factory
        self.loader = loader
        self.deserializer = deserializer if deserializer else DefaultDeserializer()
        self.cache = {}
        self.logger = logging.getLogger(self.app_name + ".config")

    def _deserialize(self, raw_value: str, value_type: Type[T]) -> T:
        return self.deserializer.deserialize(raw_value, value_type)

    def _get_value(self, option: ConfigOption):
        try:
            raw_value = self.loader.get(option.key)
        except Exception as error:
            raise ConfigurationError from error

        if raw_value is UNDEFINED:
            value = option.get_default()
        else:
            value = self._deserialize(raw_value, option.type)

        if value is UNDEFINED:
            self.loader.raise_missing_key(option.key)

        return value

    def get(self, option: ConfigOption):
        value = self.cache.get(option.key, UNDEFINED)
        if value is UNDEFINED:
            value = self._get_value(option)
            self.cache[option.key] = value
        return value

    def log(self):
        for key, value in self.cache.items():
            self.logger.info("Config value: %s=%s", key, value)
