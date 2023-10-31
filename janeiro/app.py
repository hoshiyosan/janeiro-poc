from typing import List

import click
from fastapi import FastAPI

from janeiro.config import Configuration, register_options
from janeiro.plugins.base import Plugin
from janeiro.plugins.defaults import ApiPlugin, ConfigPlugin, LoggingPlugin


class AppBuilder:
    plugins: List[Plugin]

    def __init__(
        self,
        config: Configuration,
        api_version: str = "0.0.1",
        asgi_factory_import_path: str = None,
        healthcheck_path: str = "/healthcheck",
    ):
        self.api = FastAPI(dependencies=[])
        self.cli = click.Group()
        self.config = config
        self.plugins = []
        self.built = False

        self._register_default_plugins(
            api_version=api_version,
            asgi_factory_import_path=asgi_factory_import_path,
            healthcheck_path=healthcheck_path,
        )

    def _register_default_plugins(
        self, api_version: str, asgi_factory_import_path: str, healthcheck_path: str
    ):
        self.use_plugin(LoggingPlugin())
        self.use_plugin(ConfigPlugin())
        self.use_plugin(
            ApiPlugin(
                api_version=api_version,
                asgi_factory_import_path=asgi_factory_import_path,
                healthcheck_path=healthcheck_path,
            )
        )

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

    def register_service(self, truc):
        ...

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
