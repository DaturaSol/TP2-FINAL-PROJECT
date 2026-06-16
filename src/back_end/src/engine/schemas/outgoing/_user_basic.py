"""Basic info from user."""

from pydantic import BaseModel


# TODO: Missing tests
class UserBasicEntry(BaseModel):
    """Basic user info to send back."""

    id: str
    name: str | None
    password: str | None  # NOTE: Password is hashed
