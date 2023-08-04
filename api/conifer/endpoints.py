"""Authentication API endpoints."""

from http import HTTPStatus

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse, JSONResponse

from . import services


class Health(HTTPEndpoint):
    """Health check endpoint."""

    async def get(self):
        """Check server health/readiness."""

        return PlainTextResponse("OK")


class Account(HTTPEndpoint):
    """Account endpoints."""

    async def post(self, request: Request):
        """Create a new account."""

        params = await request.json()

        # TODO: Validate params: valid email address? Password meets minimum criteria?
        # Raise 400 error if client sent missing or invalid parameters.
        email = params["email"]
        password = params["password"]

        account = services.create_account(email, password)

        return Response(status_code=HTTPStatus.CREATED)  # 201


class Login(HTTPEndpoint):
    """Login endpoints."""

    async def post(self, request: Request):
        """Login to an existing account and establish a session."""

        params = await request.json()

        # TODO: Validate params, raise 400 error for missing or invalid values
        email = params["email"]
        password = params["password"]

        session = services.login(email, password)

        return JSONResponse({
            "session": session.uuid,
            "expires_at": session.expires_at,
        })
