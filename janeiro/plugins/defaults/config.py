from janeiro.config import print_options
from janeiro.plugins.base import Plugin


class ConfigPlugin(Plugin):
    def configure(self, config):
        self.config = config

    def register(self, api, cli):
        @cli.group("config")
        def config_cli():
            """Set of commands related to app config"""

        @config_cli.command("options")
        def config_options_cmd():
            """Print available config options"""
            print_options(self.config)

        @config_cli.command("dump")
        def config_dump_cmd():
            """Dump configured values"""
            cache = self.config.get_cache()
            max_length = max(len(key) for key in cache)
            
            for key, value in cache.items():
                print("%s%s" % ((key+":").ljust(max_length+3), value))
