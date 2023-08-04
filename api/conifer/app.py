"""Application and routes."""

from starlette.applications import Starlette
from starlette.routing import Route

from . import endpoints


all_routes = [
    # TODO: API versioning, e.g. /api/v1/...
    Route("/health", endpoints.Health),
    Route("/account", endpoints.Account),
    Route("/login", endpoints.Login),
]

conifer = Starlette(routes=all_routes)
