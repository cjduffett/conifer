"""Authentication API endpoints."""

from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse


class Health(HTTPEndpoint):
    """Health check endpoint."""

    async def get(self, request):
        """Check server health/readiness."""
        return PlainTextResponse("OK")


class Account(HTTPEndpoint):
    """Account endpoints."""

    async def get(self, request):
        """Get account by ID."""

        # TODO: Query for existing Account

    async def post(self, request):
        """Create a new account."""

        # TODO: Insert new Account


class Login(HTTPEndpoint):
    """Login endpoints."""

    async def post(self, request):
        """Login to an existing account and establish a session."""

        # TODO: Insert new Session
