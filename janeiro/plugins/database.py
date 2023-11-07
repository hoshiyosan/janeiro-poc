import click
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from janeiro.config import ConfigOption
from janeiro.plugins import Plugin

DB_COMMAND_GROUP = "db"

DATABASE_URL_OPTION = ConfigOption(key="database.url", type=str)

DATABASE_AUTO_MIGRATE_OPTION = ConfigOption(
    key="database.auto_migrate", type=bool, default=False
)

session = scoped_session(session_factory=sessionmaker())


class DatabaseException(Exception):
    ...


class EntityNotFound(Exception):
    ...


class Entity(DeclarativeBase):
    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id: int):
        entity = session.query(cls).filter(cls.id == id).first()
        if entity is None:
            raise EntityNotFound(f"{cls.__name__} with id={id} not found.")
        return entity


class Resource(Entity):
    __abstract__ = True

    uuid = Column(String(36), unique=True, index=True)

    @classmethod
    def get_by_uuid(cls, uuid: str):
        entity = session.query(cls).filter(cls.id == id).first()
        if entity is None:
            raise EntityNotFound(f"{cls.__name__} with id={id} not found.")
        return entity


class DatabasePlugin(Plugin):
    __plugin__ = "database"

    def __init__(self, migrations_folder: str = None) -> None:
        super().__init__()
        self.migrations_folder = migrations_folder

    def cmd_db_init(self):
        print("Initializing DB...")

    def cmd_db_ping(self):
        print("Ping DB")

    def cmd_db_revision(self):
        print("Create DB revision")

    def cmd_db_upgrade(self):
        print("Upgrade DB...")

    def cmd_db_downgrade(self):
        print("Downgrade DB...")

    def configure(self, config):
        # parse config options
        self.database_url = config.get(DATABASE_URL_OPTION)
        self.auto_migrate = config.get(DATABASE_AUTO_MIGRATE_OPTION)
        # create engine and bind it to session
        self.engine = create_engine(self.database_url)
        session.bind = self.engine

    def extend_cli(self, cli):
        cli.declare_group(DB_COMMAND_GROUP, description="Commands to manage database")

        cli.add_command(
            self.cmd_db_init,
            name="init",
            help="Initialize database schemas and tables.",
            group=DB_COMMAND_GROUP,
        )

        cli.add_command(
            self.cmd_db_ping,
            name="ping",
            help="Performs a database connection test.",
            group=DB_COMMAND_GROUP,
        )

        if self.migrations_folder:
            cli.add_command(
                self.cmd_db_revision,
                name="revision",
                help="Automatically create a new database revision",
                group=DB_COMMAND_GROUP,
                options=[
                    click.option(
                        "-m", "--message", help="Short message describing revision"
                    )
                ],
            )

            cli.add_command(
                self.cmd_db_upgrade,
                name="upgrade",
                help="Upgrade database structure to specified revision.",
                group=DB_COMMAND_GROUP,
                options=[
                    click.option(
                        "-r",
                        "--revision",
                        default=None,
                        help="Identifier of the up revision to apply. Left empty means latest.",
                    )
                ],
            )

            cli.add_command(
                self.cmd_db_downgrade,
                name="downgrade",
                help="Downgrade database structure to specified revision.",
                group=DB_COMMAND_GROUP,
                options=[
                    click.option(
                        "-r",
                        "--revision",
                        default=None,
                        help="Identifier of the down revision to apply. Left empty means previous.",
                    )
                ],
            )
