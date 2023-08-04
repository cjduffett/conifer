"""Application and routes."""

from starlette.applications import Starlette
from starlette.routing import Route

from . import db, endpoints


def create_app() -> Starlette:
    """Initialize Conifer application and database."""
    
    db.create_tables()

    # Bind endpoints to application routes
    all_routes = [
        # TODO: API versioning, e.g. /api/v1/...
        Route("/health", endpoints.Health),
        Route("/account", endpoints.Account),
        Route("/login", endpoints.Login),
    ]

    # Create the application
    conifer_app = Starlette(routes=all_routes)
    return conifer_app


# Application object that the uvicorn ASGI will serve
conifer_app = create_app()
