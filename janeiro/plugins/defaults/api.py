import sys
import urllib.error
import urllib.request
from datetime import datetime

import click
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from janeiro.plugins.base import Plugin

DEFAULT_API_PORT = 8000


class HealthCheckDTO(BaseModel):
    start_date: datetime
    api_version: str
    uptime_in_seconds: float


class ApiPlugin(Plugin):
    def __init__(
        self,
        api_version: str = None,
        asgi_factory_import_path: str = None,
        healthcheck_path: str = "/healthcheck",
    ):
        super().__init__()
        self.start_date: datetime = None
        self.api_version = api_version
        self.asgi_factory_import_path = asgi_factory_import_path
        self.healthcheck_path = healthcheck_path

    def __add_healthcheck_endpoint(self, api: FastAPI):
        @api.on_event("startup")
        def on_api_start():
            self.start_date = datetime.utcnow()

        @api.get(self.healthcheck_path, response_model=HealthCheckDTO)
        def healthcheck():
            uptime = datetime.utcnow() - self.start_date
            return HealthCheckDTO(
                start_date=self.start_date,
                api_version=self.api_version,
                uptime_in_seconds=uptime.total_seconds(),
            )

    def __add_api_healthcheck_command(self, cli: click.Group):
        @cli.command("healthcheck")
        @click.option("--port", type=int, default=DEFAULT_API_PORT)
        def api_healthcheck_cmd(port: int):
            """Fails with exit code 1 if API is not up and running"""
            healthcheck_url = "http://127.0.0.1:%s%s" % (port, self.healthcheck_path)
            try:
                urllib.request.urlopen(healthcheck_url)
            except urllib.error.HTTPError as error:
                print(
                    "API healthcheck failed! Status code %s calling: %s"
                    % (error.getcode(), healthcheck_url),
                    file=sys.stderr,
                )
                sys.exit(1)
            except urllib.error.URLError:
                print(
                    "API healthcheck failed! No API listening on: %s" % healthcheck_url,
                    file=sys.stderr,
                )
                sys.exit(1)
            print("API healthcheck succeeded on: %s" % healthcheck_url)

    def __add_api_start_command(self, cli: click.Group, api: FastAPI):
        @cli.command("start")
        @click.option("--host", type=str, default="127.0.0.1")
        @click.option("--port", type=int, default=DEFAULT_API_PORT)
        @click.option("--debug", type=bool, is_flag=True, default=False)
        def api_start_cmd(host: str, port: int, debug: bool):
            """Start API server using uvicorn"""
            is_factory = False
            if self.asgi_factory_import_path:
                is_factory = True
            uvicorn.run(
                self.asgi_factory_import_path or api,
                host=host,
                port=port,
                reload=debug,
                factory=is_factory,
            )

    def register(self, api, cli):
        api_cli = click.Group("api", help="Set of commands related to API server")

        if self.healthcheck_path:
            self.__add_healthcheck_endpoint(api)
            self.__add_api_healthcheck_command(api_cli)

        self.__add_api_start_command(api_cli, api)

        cli.add_command(api_cli)
