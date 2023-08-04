"""Authentication API endpoints."""

from http import HTTPStatus

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse, JSONResponse

from . import services


class Health(HTTPEndpoint):
    """Health check endpoint."""

    async def get(self, request: Request):
        """Check server health/readiness."""

        return PlainTextResponse("OK")


class Account(HTTPEndpoint):
    """Account endpoints."""

    async def post(self, request: Request):
        """Create a new account."""

        params = await request.json()

        # TODO: Handle missing or blank params that would cause a KeyError here
        email = params["email"]
        password = params["password"]

        services.create_account(email, password)

        return Response(status_code=HTTPStatus.CREATED)  # 201


class Login(HTTPEndpoint):
    """Login endpoints."""

    async def post(self, request: Request):
        """Login to an existing account and establish a session."""

        params = await request.json()

        email = params["email"]
        password = params["password"]

        session = services.login(email, password)

        # TODO: Create schemas for requests and responses, compatible with OpenAPI spec:
        # https://www.starlette.io/schemas/
        return JSONResponse({
            "session": session.uuid,
            "expires_at": str(session.expires_at),
        })
