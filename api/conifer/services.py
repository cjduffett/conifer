"""Authentication service methods."""

import datetime as dt
from http import HTTPStatus
from typing import Optional
from uuid import uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from . import db, models

DEFAULT_SESSION_TIMEOUT_SECONDS = 3600  # 1 hour


def create_account(email: str, password: str) -> models.Account:
    """Create a new user account."""

    # TODO: More validation of params: valid email address? Password meets minimum criteria?
    if not email or not password:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid email or password")

    # One-way hashing of password for secure storage
    hasher = PasswordHasher()
    hashed_password = hasher.hash(password)
    
    account = models.Account(
        email=email,
        password=hashed_password.encode("utf-8"),  # bytes
    )

    # TODO: Handle integrity error if an account with that email already exists
    try:
        with db.session() as db_session:
            db_session.add(account)
            db_session.commit()
    except IntegrityError:
        # Account with that email already exists
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Account with that email already exists")

    # TODO: Send "Account created" email confirmation
    return account


def get_account(email: str) -> Optional[models.Account]:
    """Get an account by email. Returns None if the account does not exist."""

    with db.session() as db_session:
        stmt = select(models.Account).where(models.Account.email == email)
        result = db_session.execute(stmt)
        account = result.scalar_one_or_none()

    return account


def login(email: str, password: str) -> models.Session:
    """Create a new session for an existing account."""

    # Find existing account
    account = get_account(email)

    if not account:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid email or password")
    
    # Compare passwords
    hasher = PasswordHasher()

    try:
        match = hasher.verify(account.password, password)
    except VerifyMismatchError:
        match = False

    if not match:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid email or password")
    
    # Password was valid, issue a new session
    session = create_session(account)
    return session


def create_session(account: models.Account) -> models.Session:
    """Create a new session."""

    session_uuid = uuid4().hex
    created_at = utc_now()
    expires_at = created_at + dt.timedelta(seconds=DEFAULT_SESSION_TIMEOUT_SECONDS)
    
    new_session = models.Session(
        uuid=session_uuid,
        account=account,
        created_at=created_at,
        expires_at=expires_at,
    )

    with db.session() as db_session:
        db_session.add(new_session)
        db_session.commit()

    return new_session


def utc_now() -> dt.datetime:
    """Current timestamp in UTC."""

    return dt.datetime.now(tz=dt.timezone.utc)
