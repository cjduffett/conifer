"""Authentication service methods."""

from argon2 import PasswordHasher

from . import db, models


def create_account(email: str, password: str) -> models.Account:
    """Create a new user account."""

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


def login(email: str, password: str) -> models.Session:
    """Create a new session for an existing account."""

    # TODO
