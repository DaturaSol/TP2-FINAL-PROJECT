# ./src/back_end/src/engine/schemas/ingoing/_logging.py
"""Ingoing schema for user registration.

HU01: validates and normalises the registration fields.
"""

from pydantic import BaseModel, field_validator

from ._validators import normalise_email, validate_sha256_digest


class LoggingEntry(BaseModel):
    """Information passed when registering a new user account."""

    name: str | None = None
    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalise and validate the e-mail address."""
        # Pre:  v is the raw e-mail field from the incoming payload
        # Post: returns the normalised e-mail or raises ValueError
        return normalise_email(v)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate that the password is a SHA-256 hex digest.

        The frontend hashes the plaintext with SHA-256 before sending, so the
        plaintext never crosses the wire and strength rules must be enforced
        on the frontend.
        """
        # Pre:  v is the raw password field from the incoming payload
        # Post: returns the normalised digest or raises ValueError
        return validate_sha256_digest(v)
