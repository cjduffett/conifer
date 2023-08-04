"""Authentication API endpoints."""

from http import HTTPStatus

from argon2 import PasswordHasher
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse

from . import db, models


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
        email = params["email"]
        password = params["password"]

        # One-way hashing of password for secure storage
        hasher = PasswordHasher()
        hashed_password = hasher.hash(password)
        
        account = models.Account(
            email=email,
            password=hashed_password.encode("utf-8"),  # bytes
        )

        with db.session() as session:
            session.add(account)
            session.commit()

        return Response(status_code=HTTPStatus.CREATED)  # 201


class Login(HTTPEndpoint):
    """Login endpoints."""

    async def post(self, request):
        """Login to an existing account and establish a session."""

        # TODO: Insert new Session
        return PlainTextResponse("Session(abc123)")
