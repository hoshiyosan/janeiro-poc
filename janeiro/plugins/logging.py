from janeiro.config import ConfigOption
from janeiro.plugins.base import Plugin


LOG_LEVEL_OPTION = ConfigOption(key="log.level", description="", type=str)
LOG_FORMAT_OPTION = ConfigOption(key="log.format", description="", type=str)

class LoggingPlugin(Plugin):
    options = [LOG_LEVEL_OPTION, LOG_FORMAT_OPTION]
