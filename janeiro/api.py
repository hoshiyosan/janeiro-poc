from typing import Any, Callable, Dict, List, Tuple, Type

from fastapi import APIRouter, Depends, params
from starlette.middleware.base import BaseHTTPMiddleware


class ApiRegistry:
    dependencies: List[params.Depends]
    middlewares: List[Tuple[Type[BaseHTTPMiddleware], Dict[str, Any]]]

    def __init__(self):
        self.router = APIRouter(tags=["extensions"])
        self.dependencies = []
        self.middlewares = []

    @property
    def add_api_route(self):
        return self.router.add_api_route

    def add_dependency(self, dependency: Callable):
        self.dependencies.append(Depends(dependency))

    def add_middleware(self, middleware: BaseHTTPMiddleware, **options):
        self.middlewares.append((middleware, options))

    def get_dependencies(self):
        return self.dependencies

    def get_middlewares(self):
        return self.middlewares
