"""Database models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase):
    """Base class for all declarative database models.
    
    See: https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models

    Column types and nullability are derived from the type annotations:
    https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapped-column-derives-the-datatype-and-nullability-from-the-mapped-annotation
    """


class Account(BaseModel):
    """A user account."""

    __tablename__ = "account"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO: Consider refactoring email into a separate table to allow for multiple email addresses,
    # for example a communication email vs. authentication email; allowing both work and personal
    # email addresses, perhaps no email address at all (if SSO).
    email: Mapped[str] = mapped_column(unique=True)

    # Guidelines for hashing, salting, peppering passwords:
    # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
    password: Mapped[bytes] = mapped_column()

    # TODO: Track 'password_set_at', 'last_login', login attempts, password history; other
    # attributes that help with password rotation and detection of unusual activity.

    # TODO: Consider refactoring authentication methods into separate models, for example
    # to distinguish between email/password logins, SSO logins (SAML, OIDC), etc.

    def __repr__(self) -> str:
        return f"Account(id={self.id}, email={self.email})"


class Session(BaseModel):
    """A session."""

    __tablename__ = "session"

    # Unique session ID can be sent in 'Authorization' header or used in URLs for all
    # authenticated endpoints, for example: GET /api/v1/<session>/account
    uuid: Mapped[UUID] = mapped_column(primary_key=True)

    # Current design allows for multiple active sessions per-account (e.g desktop + mobile).
    # Also allows us to track session history over time, query an Account's previous sessions.
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    # ORM relationships for convenience, see:
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
    account: Mapped[Account] = relationship("Account")

    # Timestamps are in UTC
    created_at: Mapped[datetime] = mapped_column()

    # For a timeout after n minutes of inactivity, this timestamp can be periodically updated
    # as the user is active and making authenticated requests to the application.
    expires_at: Mapped[datetime] = mapped_column()

    def __repr__(self) -> str:
        return f"Session(uuid={self.uuid}, account_id={self.account_id})"
