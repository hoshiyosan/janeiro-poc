from contextvars import ContextVar
from logging import Logger, getLogRecordFactory, setLogRecordFactory
from uuid import uuid4

from fastapi import Header, Request
from starlette.middleware.base import BaseHTTPMiddleware

from janeiro.plugins import Plugin

REQUEST_ID_CTX = ContextVar("REQUEST_ID")

old_factory = getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)

    try:
        request_id = REQUEST_ID_CTX.get()
    except LookupError:
        request_id = ""

    record.request_id = request_id
    return record


setLogRecordFactory(record_factory)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: Logger, dispatch=None):
        super().__init__(app, dispatch)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        request_id = uuid4().hex
        token = REQUEST_ID_CTX.set(request_id)
        response = await call_next(request)
        self.logger.info(
            "%s %s  %s",
            request.method,
            request.url.path,
            response.status_code,
        )
        REQUEST_ID_CTX.reset(token)
        return response


class LoggingPlugin(Plugin):
    __plugin__ = "logging"

    async def dependency_logging(
        self,
        request: Request,
        x_request_id: str = Header(None, description="Request ID"),
    ):
        self.logger.debug(
            "%s %s  ...",
            request.method,
            request.url.path,
        )

    def extend_api(self, api):
        api.add_dependency(self.dependency_logging)
        api.add_middleware(LoggingMiddleware, logger=self.logger)
