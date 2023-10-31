import json
import logging
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, Request

from janeiro.config import ConfigOption
from janeiro.plugins.base import Plugin

LOG_LEVEL_OPTION = ConfigOption(
    key="log.level", description="Select logs level (~= verbosity)", type=str
)
LOG_FORMAT_OPTION = ConfigOption(
    key="log.format",
    description="Select logs format (choose from: json,text)",
    type=str,
)

REQUEST_ID_CTX = ContextVar("REQUEST_ID")


def request_id_dependency(
    x_request_id: str = Header(
        None,
        description="Request ID used for request tracing. (will be available in logs)",
    )
):
    ...


class JsonFormatter(logging.Formatter):
    def formatMessage(self, record):
        _log = record.__dict__.copy()
        _log["message"] = _log.pop("msg") % record.__dict__
        _log.pop("args")
        return json.dumps(_log)


class LogFormatter(logging.Formatter):
    def formatMessage(self, record):
        message = self._style.format(record)
        return message % record.__dict__


class LoggingPlugin(Plugin):
    options = [LOG_LEVEL_OPTION, LOG_FORMAT_OPTION]

    def configure(self, config):
        self.log_format = config.get(LOG_FORMAT_OPTION)
        self.log_level = config.get(LOG_LEVEL_OPTION)

    def __setup_logging(self):
        stream = logging.StreamHandler()

        if self.log_format == "text":
            stream.formatter = LogFormatter(
                "%(asctime)s --- %(levelname)s --- %(message)s"
            )
        elif self.log_format == "json":
            stream.formatter = JsonFormatter()

        logging.basicConfig(level=self.log_level, handlers=[stream], force=True)

    def __add_request_tracing(self, api: FastAPI):
        api.router.dependencies.append(Depends(request_id_dependency))

        @api.middleware("http")
        async def tracing_middleware(request: Request, call_next):
            request_id = request.headers.get("X-Request-Id")
            if request_id is None:
                request_id = uuid4().hex
            ctx_token = REQUEST_ID_CTX.set(request_id)
            response = await call_next(request)
            REQUEST_ID_CTX.reset(ctx_token)
            return response

    def register(self, api, cli):
        self.__setup_logging()
        self.__add_request_tracing(api)
