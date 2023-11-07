import sys
import urllib.error
import urllib.request
from datetime import datetime

import click
import uvicorn
from pydantic import BaseModel

from janeiro.plugins import Plugin

API_COMMAND_GROUP = "api"

PORT_CMD_OPTION = click.option(
    "--port",
    type=int,
    default=8000,
    help="Port on which API server listens",
)


class ApiPlugin(Plugin):
    __plugin__ = "api"

    def __init__(self, asgi_factory: str):
        self.asgi_factory = asgi_factory

    def cmd_start_api(self, host: str, port: int, debug: bool, workers: int):
        uvicorn.run(
            self.asgi_factory,
            host=host,
            port=port,
            reload=debug,
            factory=True,
            access_log=False,
            log_config=None,
            workers=workers,
        )

    def extend_cli(self, cli):
        cli.declare_group(group=API_COMMAND_GROUP, description="Commands to manage API")

        cli.add_command(
            self.cmd_start_api,
            name="start",
            help="Start API using ASGI server.",
            group=API_COMMAND_GROUP,
            options=[
                PORT_CMD_OPTION,
                click.option("--host", type=str, default="127.0.0.1"),
                click.option("--debug", type=bool, is_flag=True, default=False),
                click.option(
                    "-w",
                    "--workers",
                    type=int,
                    default=None,
                    help="Number of workers processes for the ASGI server.",
                ),
            ],
        )


START_DATE = datetime.utcnow()


class HealthCheckDTO(BaseModel):
    version: str
    uptime_seconds: float


class HealthCheckPlugin(Plugin):
    __plugin__ = "healthcheck"

    def __init__(self, api_version: str, healthcheck_path: str = "/healthcheck"):
        self.api_version = api_version
        self.healthcheck_path = healthcheck_path

    def cmd_healthcheck_api(self, port: int):
        healthcheck_url = "http://127.0.0.1:%s%s" % (port, self.healthcheck_path)
        try:
            urllib.request.urlopen(healthcheck_url)
        except urllib.error.HTTPError as error:
            click.echo(
                "API healthcheck failed! Status code %s calling: %s"
                % (error.getcode(), healthcheck_url),
                file=sys.stderr,
            )
            sys.exit(1)
        except urllib.error.URLError:
            click.echo(
                "API healthcheck failed! No API listening on: %s" % healthcheck_url,
                file=sys.stderr,
            )
            sys.exit(1)
        click.echo("API healthcheck succeeded on: %s" % healthcheck_url)

    def endpoint_healthcheck(self):
        current_date = datetime.utcnow()
        return HealthCheckDTO(
            version=self.api_version,
            uptime_seconds=(current_date - START_DATE).total_seconds(),
        )

    def extend_cli(self, cli):
        cli.declare_group(group=API_COMMAND_GROUP, description="Commands to manage API")

        cli.add_command(
            self.cmd_healthcheck_api,
            name="health",
            help="Healthcheck API and fails with exit code 1 if API is down.",
            group=API_COMMAND_GROUP,
            options=[PORT_CMD_OPTION],
        )

    def extend_api(self, api):
        api.add_api_route(
            "/healthcheck", self.endpoint_healthcheck, response_model=HealthCheckDTO
        )
