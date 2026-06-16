# ./src/back_end/src/engine/schemas/ingoing/_database.py
"""Database expected response."""

from pydantic import BaseModel


# TODO: test this, add other methods
class LoggingEntry(BaseModel):
    """Information passed when logging."""

    name: str | None
    email: str
    password: str
