from typing import List

import click
from fastapi import FastAPI

from janeiro.config import ConfigOption, Configuration, register_options


class Plugin:
    """Interface that implements lifecycle of a plugin."""

    options: List[ConfigOption] = None

    def __init__(self):
        ...

    def configure(self, config: Configuration):
        """Configure plugin from app config.

        Method that is called for all plugins before starting each plugin's lifecycle
        to validate global configuration immediately when application starts.
        """

    def register(self, api: FastAPI, cli: click.Group):
        ...
