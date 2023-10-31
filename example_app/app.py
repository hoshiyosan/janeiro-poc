from example_app.domain.accounts.service import AccountService
from janeiro.app import AppBuilder
from janeiro.config import Configuration, package_relative_path
from janeiro.config.loader.environment import EnvironmentConfigLoader
from janeiro.plugins.database import DatabasePlugin

app_builder = AppBuilder(
    config=Configuration(loader=EnvironmentConfigLoader()),
    asgi_factory_import_path="example_app.app:app_builder.create_api",
)

app_builder.use_plugin(
    DatabasePlugin(migrations_folder=package_relative_path("db/migrations"))
)

app_builder.register_service(AccountService)
