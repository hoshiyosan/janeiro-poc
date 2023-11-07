import example.api
from janeiro import Application
from janeiro.config import Configuration
from janeiro.config.loaders.environment import EnvironmentConfigLoader
from janeiro.plugins.auth import AuthPlugin
from janeiro.plugins.database import DatabasePlugin
from janeiro.plugins.logging import LoggingPlugin

app = Application(
    api_title="example",
    api_version="0.0.1",
    openapi_url="/",
    openapi_tags={"accounts": "Manage accounts"},
    config=Configuration(
        app_name="example",
        asgi_factory="example.main:app.get_api",
        loader=EnvironmentConfigLoader(prefix="example"),
    ),
)

app.use_plugin(LoggingPlugin())
app.use_plugin(DatabasePlugin())
app.use_plugin(AuthPlugin())

app.include_router(example.api.router)

cli = app.get_cli()

if __name__ == "__main__":
    cli()

# uvicorn.run(api)
