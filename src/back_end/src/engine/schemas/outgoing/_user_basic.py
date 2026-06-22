# ./src/back_end/src/engine/schemas/outgoing/_user_basic.py
"""Basic user info returned to the frontend.

HU01: sent back after successful account creation.
"""

from pydantic import BaseModel


class UserBasicEntry(BaseModel):
    """Basic user info to send back after registration."""

    id: int
    name: str | None
    email: str
