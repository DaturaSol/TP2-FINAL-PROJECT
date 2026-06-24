# ./src/back_end/src/engine/schemas/ingoing/_logging.py
"""Ingoing schema for user registration.

HU01: validates and normalises the registration fields.
"""

import re

from pydantic import BaseModel, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MIN_PASSWORD_LEN = 8


class LoggingEntry(BaseModel):
    """Information passed when registering a new user account."""

    name: str | None = None
    email: str
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalise and validate the e-mail address.

        Args:
            v: Raw e-mail string from the payload.

        Returns:
            Stripped and lowercased e-mail address.

        Raises:
            ValueError: If the value is not a valid e-mail address.
        """
        # Pre:  v is the raw e-mail field from the incoming payload
        # Post: returns v.strip().lower() or raises ValueError
        normalised = v.strip().lower()
        if not _EMAIL_RE.match(normalised):
            raise ValueError(f"Invalid e-mail address: {v!r}")
        return normalised

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Enforce a minimum password length.

        Args:
            v: Raw password string from the payload.

        Returns:
            The password unchanged if valid.

        Raises:
            ValueError: If the password is shorter than the minimum length.
        """
        # Pre:  v is the raw password field from the incoming payload
        # Post: returns v unchanged or raises ValueError
        if len(v) < _MIN_PASSWORD_LEN:
            raise ValueError(
                f"Password must be at least {_MIN_PASSWORD_LEN} characters."
            )
        return v
