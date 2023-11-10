import logging
from contextlib import asynccontextmanager
from typing import Dict, List

import click
from fastapi import APIRouter, FastAPI

from janeiro.api import ApiRegistry
from janeiro.cli import CliRegistry
from janeiro.config import Configuration
from janeiro.plugins import Plugin
from janeiro.plugins.defaults import ApiPlugin, HealthCheckPlugin


def build_tags_list(tags: Dict[str, str]):
    if tags is None:
        return
    return [
        {"name": tag, "description": description} for tag, description in tags.items()
    ]


class Application:
    api: FastAPI
    cli: click.Group
    config: Configuration
    plugins: List[Plugin]
    routers: List[APIRouter]

    def __init__(
        self,
        *,
        config: Configuration,
        api_title: str,
        api_version: str,
        openapi_url: str = "/",
        openapi_tags: Dict[str, str] = None,
    ):
        self.api = None
        self.cli = None
        self.config = config
        self.routers = []
        self.plugins = []
        self.plugins_configured = False
        self.api_config = {
            "title": api_title,
            "version": api_version,
            "docs_url": openapi_url,
            "openapi_tags": build_tags_list(openapi_tags),
        }
        self.logger = logging.getLogger(self.config.app_name)

    @asynccontextmanager
    async def _lifespan(self, api: FastAPI):
        yield

        for plugin in self.plugins:
            plugin.cleanup()

    def _register_default_plugins(self):
        self.use_plugin(ApiPlugin(asgi_factory=self.config.asgi_factory))
        self.use_plugin(HealthCheckPlugin(api_version=self.api_config["version"]))

    def configure_plugins(self):
        for plugin in self.plugins:
            self.logger.info("Plugin enabled: %s", plugin.__plugin__)

        if self.plugins_configured:
            return

        self._register_default_plugins()

        for plugin in self.plugins:
            plugin.setup(self.config)
            self.logger.debug("Plugin configured: %s", plugin.__plugin__)

        self.config.log()

    def use_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)

    def build_api(self):
        self.configure_plugins()

        api_registry = ApiRegistry()
        for plugin in self.plugins:
            plugin.extend_api(api_registry)

        self.api = FastAPI(
            dependencies=api_registry.get_dependencies(),
            lifespan=self._lifespan,
            **self.api_config,
        )
        for middleware, options in api_registry.get_middlewares():
            self.api.add_middleware(middleware, **options)

        self.api.include_router(api_registry.router)

        for router in self.routers:
            self.api.include_router(router)

    def build_cli(self):
        self.configure_plugins()

        cli_registry = CliRegistry()
        for plugin in self.plugins:
            plugin.extend_cli(cli_registry)

        self.cli = click.Group(help=cli_registry.description)

        for name, commands in cli_registry.group_commands.items():
            description = None
            if name is not None:
                description = cli_registry.group_descriptions.get(name)

            group = self.cli if name is None else click.Group(name, help=description)
            for command in commands:
                group.add_command(command)

            if name:
                self.cli.add_command(group)

    def get_api(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(request_id)-32s ::: %(levelname)-6s ::: %(message)s",
            # format="%(asctime)s ::: %(levelname)-6s ::: %(name)s ::: %(message)s",
            force=True,
        )
        if self.api is None:
            self.build_api()
        return self.api

    def get_cli(self):
        logging.basicConfig(
            level=logging.WARNING,
            force=True,
        )

        if self.cli is None:
            self.build_cli()

        return self.cli

    def include_router(self, router: APIRouter):
        return self.routers.append(router)
