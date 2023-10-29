import uvicorn
from janeiro.plugins.base import Plugin

class ApiCliPlugin(Plugin):
    def register(self, api, cli):
        @cli.group("api")
        def api_cli():
            ...
        
        @api_cli.command("start")
        def api_start_cmd():
            uvicorn.run(api)
