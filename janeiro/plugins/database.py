import os
import click
import alembic.config

from janeiro.config import ConfigOption, Configuration
from janeiro.plugins.base import Plugin

DATABASE_AUTO_MIGRATE_OPTION = ConfigOption(
    key="database.auto_migrate",
    description=(
        "Whether to apply database migration at application startup.",
        "Warning: avoid using this option if your app has multiple ",
        "components/instances using same DB.",
    ),
    type=bool,
)

DATABASE_URL_OPTION = ConfigOption(
    key="database.url",
    description=(
        "SQLAlchemy database URL.",
        "See following documentation:",
        "https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls",
    ),
    type=str,
)


class DatabasePlugin(Plugin):
    options = [
        DATABASE_URL_OPTION, DATABASE_AUTO_MIGRATE_OPTION
    ]

    def __init__(self, migrations_folder: str):
        self.migrations_folder = migrations_folder
    
    def configure(self, config: Configuration):
        self.config = config

    def _get_alembic_config(self):
        alembic_config = alembic.config.Config()
        alembic_config.set_main_option("script_location", os.path.join(self.migrations_folder))
        alembic_config.set_main_option("sqlalchemy.url", self.config.get(DATABASE_URL_OPTION))
        return alembic_config

    
    def register(self, api, cli):
        @cli.group("db")
        def db_cli():
            ...

        @db_cli.command("init")
        def db_init_cmd():
            ...

        @db_cli.command("revision")
        @click.option("-m", "--message")
        def db_revision_cmd(message: str = None):
            import alembic.command
            config = self._get_alembic_config()
            alembic.command.revision(config, message)

        @db_cli.command("upgrade")
        @click.option("--revision")
        def db_upgrade_cmd(revision: str = None):
            import alembic.command
            config = self._get_alembic_config()
            if revision is None:
                from alembic.script import ScriptDirectory
                directory = ScriptDirectory.from_config(config)
                revision = next(script.revision for script in directory.walk_revisions())
            alembic.command.upgrade(config, revision)

        @db_cli.command("downgrade")
        @click.option("--revision")
        def db_downgrade_cmd(revision: str):
            ...
