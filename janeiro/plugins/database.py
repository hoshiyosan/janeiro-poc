import os

import alembic.command
import alembic.config
import click
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

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


session = scoped_session(session_factory=sessionmaker())


class Entity(DeclarativeBase):
    ...


class DatabasePlugin(Plugin):
    """Plugin that provides database connection in controllers.

    Additionally brings a command group 'database' with db migration targets.

    Arguments:
        migrations_folder: Path to folder containing alembic .env file.
    """

    options = [DATABASE_URL_OPTION, DATABASE_AUTO_MIGRATE_OPTION]

    def __init__(self, migrations_folder: str):
        super().__init__()
        self.migrations_folder = migrations_folder

    def configure(self, config: Configuration):
        self.config = config
        self.database_url = self.config.get(DATABASE_URL_OPTION)
        self.auto_migrate = self.config.get(DATABASE_AUTO_MIGRATE_OPTION)

    def _get_alembic_config(self):
        alembic_config = alembic.config.Config()
        alembic_config.set_main_option(
            "script_location", os.path.join(self.migrations_folder)
        )
        alembic_config.set_main_option("sqlalchemy.url", self.database_url)
        return alembic_config

    def _upgrade_db(self, revision: str = None):
        config = self._get_alembic_config()
        if revision is None:
            directory = ScriptDirectory.from_config(config)
            revision = next(script.revision for script in directory.walk_revisions())
        alembic.command.upgrade(config, revision)

    def register(self, api, cli):
        self.engine = create_engine(self.database_url)
        session.bind = self.engine

        @cli.group("db")
        def db_cli():
            """Set of commands to manage database"""

        @db_cli.command("init")
        def db_init_cmd():
            """Initialise database schemas (without alembic)."""
            Entity.metadata.drop_all(self.engine)
            Entity.metadata.create_all(self.engine)

        @db_cli.command("revision")
        @click.option("-m", "--message")
        def db_revision_cmd(message: str = None):
            """Auto generate a new database revision that reflects changes with DB."""
            config = self._get_alembic_config()
            alembic.command.revision(config, message, autogenerate=True)

        @db_cli.command("upgrade")
        @click.option("--revision")
        def db_upgrade_cmd(revision: str = None):
            """Upgrade database to given revision (defaults to latest)"""
            self._upgrade_db(revision)

        @db_cli.command("downgrade")
        @click.option("--revision")
        def db_downgrade_cmd(revision: str):
            """Downgrade database to given revision (default to one revision down)"""

        if self.auto_migrate:
            self._upgrade_db()
