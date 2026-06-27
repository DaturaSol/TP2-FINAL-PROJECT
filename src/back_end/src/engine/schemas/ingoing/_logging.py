# ./src/back_end/src/engine/schemas/ingoing/_logging.py
"""Ingoing schema for user registration.

HU01: validates and normalises the registration fields.
"""

import re

from pydantic import BaseModel, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# The frontend hashes the user's plaintext password with SHA-256 before
# sending it, so what we receive in the ``password`` field is always a
# 64-character hexadecimal digest (lowercase). We validate that *shape*.
_SHA256_HEX_LEN = 64
_SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


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
        """Validate that the password is a SHA-256 hex digest.

        The frontend hashes the plaintext password with SHA-256 and sends
        only the resulting hex digest, so the plaintext never travels over
        the wire. We therefore validate the *shape* of that digest here.

        Password-strength rules (minimum length, complexity, ...) can no
        longer be checked by the backend, since it never sees the plaintext;
        those must be enforced on the frontend, before hashing.

        Args:
            v: Raw password field from the payload (expected: a SHA-256
                hex digest produced by the frontend).

        Returns:
            The digest, stripped and lowercased.

        Raises:
            ValueError: If the value is not a valid SHA-256 hex digest.
        """
        # Pre:  v is the raw password field from the incoming payload
        # Post: returns the normalised (lowercase) digest, or raises
        #       ValueError when v is not 64 hexadecimal characters
        normalised = v.strip().lower()
        if not _SHA256_HEX_RE.match(normalised):
            raise ValueError(
                "Password must be a SHA-256 hex digest "
                f"({_SHA256_HEX_LEN} hexadecimal characters)."
            )
        return normalised
