from janeiro.plugins.base import Plugin


class HealthCheckPlugin(Plugin):
    def __init__(self, healthcheck_path: str = "/healthcheck"):
        self.healthcheck_path = healthcheck_path
