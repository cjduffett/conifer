"""Database engine and session."""

import os

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import BaseModel


# Factory for creating new database connections, manages the connection pool for us.
# echo=True logs all SQL emitted by the ORM for debugging. Disable in production.
engine = create_engine(os.environ["CONIFER_DB_URL"], echo=True)


def create_tables():
    """Create database tables based on current models."""
    
    # In production, replace this with a database migration system like Alembic. Apply database
    # changes independently from starting the application. See: https://alembic.sqlalchemy.org/en/latest/
    BaseModel.metadata.create_all(engine)


@contextmanager
def session():
    """Create a new database session, ensure the session is closed when finished."""

    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
