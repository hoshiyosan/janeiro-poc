from janeiro.app import AppBuilder
from janeiro.config import Configuration, EnvironmentConfigLoader, package_relative_path
from janeiro.plugins.config import ConfigPlugin
from janeiro.plugins.database import DatabasePlugin
from janeiro.plugins.healthcheck import HealthCheckPlugin
from janeiro.plugins.logging import LoggingPlugin
from janeiro.plugins.api_cli import ApiCliPlugin

app_builder = AppBuilder(config=Configuration(loader=EnvironmentConfigLoader()))

app_builder.use_plugin(ApiCliPlugin())
app_builder.use_plugin(LoggingPlugin())
app_builder.use_plugin(HealthCheckPlugin())
app_builder.use_plugin(ConfigPlugin())
app_builder.use_plugin(
    DatabasePlugin(migrations_folder=package_relative_path("db/migrations"))
)
