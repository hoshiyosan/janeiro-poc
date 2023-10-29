from typing import List

import click
from fastapi import FastAPI

from janeiro.config import ConfigOption, Configuration, register_options


class Plugin:
    options: List[ConfigOption] = None

    def __init__(self):
        ...

    def configure(self, config: Configuration):
        ...

    def register(self, api: FastAPI, cli: click.Group):
        ...
