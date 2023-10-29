from typing import List

import click
from fastapi import FastAPI

from janeiro.config import Configuration, register_options
from janeiro.plugins.base import Plugin


class AppBuilder:
    plugins: List[Plugin]

    def __init__(self, config: Configuration):
        self.api = FastAPI()
        self.cli = click.Group()
        self.config = config
        self.plugins = []
        self.built = False

    def _ensure_not_built(self):
        if self.built == True:
            raise Exception(
                "You can't use this method once build method of AppBuilder has been called"
            )

    def use_plugin(self, plugin: Plugin):
        self._ensure_not_built()
        if plugin.options:
            register_options(*plugin.options)
        self.plugins.append(plugin)

    def build_app(self):
        if self.built:
            return

        for plugin in self.plugins:
            plugin.configure(self.config)
            plugin.register(self.api, self.cli)

        self.built = True

    def create_api(self):
        self.build_app()
        return self.api

    def create_cli(self):
        self.build_app()
        return self.cli
