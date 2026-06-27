# ./src/back_end/src/engine/schemas/ingoing/_validators.py
"""Shared field validators for ingoing schemas.

Registration (LoggingEntry) and login (LoginRequest) accept the same e-mail
and password shapes, so the validation lives here and is reused by both.
"""

import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# The frontend hashes the user's plaintext password with SHA-256 before
# sending it, so the ``password`` field is always a 64-character hexadecimal
# digest (lowercase). We validate that *shape* — never the plaintext, which
# the backend no longer sees.
_SHA256_HEX_LEN = 64
_SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


def normalise_email(v: str) -> str:
    """Strip, lowercase and validate an e-mail address.

    Args:
        v: Raw e-mail string from the payload.

    Returns:
        The stripped, lowercased e-mail address.

    Raises:
        ValueError: If the value is not a valid e-mail address.
    """
    # Pre:  v is the raw e-mail field from the incoming payload
    # Post: returns v.strip().lower() or raises ValueError
    normalised = v.strip().lower()
    if not _EMAIL_RE.match(normalised):
        raise ValueError(f"Invalid e-mail address: {v!r}")
    return normalised


def validate_sha256_digest(v: str) -> str:
    """Strip, lowercase and validate a SHA-256 hex digest.

    Strength rules (length, complexity, ...) cannot be checked here because
    the backend only ever sees the hash; they belong on the frontend, before
    hashing.

    Args:
        v: Raw password field from the payload (expected: a SHA-256 hex
            digest produced by the frontend).

    Returns:
        The digest, stripped and lowercased.

    Raises:
        ValueError: If the value is not a valid SHA-256 hex digest.
    """
    # Pre:  v is the raw password field from the incoming payload
    # Post: returns the normalised (lowercase) digest, or raises ValueError
    #       when v is not 64 hexadecimal characters
    normalised = v.strip().lower()
    if not _SHA256_HEX_RE.match(normalised):
        raise ValueError(
            "Password must be a SHA-256 hex digest "
            f"({_SHA256_HEX_LEN} hexadecimal characters)."
        )
    return normalised
