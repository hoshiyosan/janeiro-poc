from fastapi import Header

from janeiro.plugins import Plugin


async def auth_dependency(x_auth_token: str = Header(None, description="Auth token")):
    ...


class AuthPlugin(Plugin):
    __plugin__ = "auth"

    def extend_api(self, api):
        api.add_dependency(auth_dependency)
