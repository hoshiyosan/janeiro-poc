from logging import getLogger

from janeiro.api import ApiRegistry
from janeiro.cli import CliRegistry
from janeiro.config import Configuration


class PluginType(type):
    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)


class Plugin(metaclass=PluginType):
    __plugin__: str = None

    def setup(self, config: Configuration):
        self._setup_logging(config)
        self.configure(config)

    def _setup_logging(self, config: Configuration):
        logger_name = config.app_name + "." + self.__plugin__
        self.logger = getLogger(logger_name)

    def configure(self, config: Configuration):
        """Method called right at app startup to load user-defined configuration."""

    def extend_api(self, api: ApiRegistry):
        """Method that let plugin register endpoints, middlewares and dependencies."""

    def extend_cli(self, cli: CliRegistry):
        """Method that let plugin register commands."""

    def cleanup(self):
        """Method called before app shutdown."""
