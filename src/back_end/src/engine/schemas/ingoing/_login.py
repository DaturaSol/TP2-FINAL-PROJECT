# ./src/back_end/src/engine/schemas/ingoing/_login.py
"""Ingoing schema for the login endpoint.

HU02: validates the flat login body the frontend posts to /login — an
e-mail and the SHA-256 digest of the password (the same digest used at
registration). Unlike registration, login is not wrapped in the webhook
envelope.
"""

from pydantic import BaseModel, field_validator

from ._validators import normalise_email, validate_sha256_digest


class LoginRequest(BaseModel):
    """Credentials posted to POST /login."""

    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalise and validate the e-mail address."""
        # Pre:  v is the raw e-mail field from the login body
        # Post: returns the normalised e-mail or raises ValueError
        return normalise_email(v)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate that the password is a SHA-256 hex digest."""
        # Pre:  v is the raw password field from the login body
        # Post: returns the normalised digest or raises ValueError
        return validate_sha256_digest(v)
