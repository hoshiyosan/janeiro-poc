from typing import Callable

import click


class CliRegistry:
    def __init__(self):
        self.description = None
        self.group_descriptions = {}
        self.group_commands = {}

    def declare_group(self, group: str, *, description: str):
        if self.group_descriptions.get(group) is None:
            self.group_descriptions[group] = description

    def add_command(
        self,
        command: Callable,
        *,
        name: str,
        help: str,
        options: list = None,
        group: str = None,
    ):
        command_list = self.group_commands.get(group)
        if command_list is None:
            command_list = self.group_commands[group] = []

        command = click.Command(name=name, help=help, callback=command)
        if options:
            for option in options:
                command = option(command)
        command_list.append(command)
