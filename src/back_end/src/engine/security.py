# ./src/back_end/src/engine/security.py
"""Password hashing and verification utilities.

Uses PBKDF2-HMAC-SHA256 from the standard library — no external
dependencies required.

Two-layer scheme: the frontend already hashes the user's plaintext password
with SHA-256 (so the plaintext never crosses the network), and the functions
here add a salted, slow PBKDF2 layer on top before the value is stored. The
client-side SHA-256 protects the plaintext in transit; the server-side salted
PBKDF2 protects the database if it ever leaks. The ``password`` argument below
is therefore the client-side SHA-256 digest, not the raw plaintext — but the
functions treat it as an opaque string and would work the same on either.

HU01: provides the cryptographic primitives for user registration.
"""

import base64
import hashlib
import hmac
import secrets

_ALGORITHM = "sha256"
_ITERATIONS = 600_000  # OWASP 2023 minimum for PBKDF2-HMAC-SHA256
_SALT_BYTES = 16
_SEP = "$"


def hash_password(password: str) -> str:
    """Hash a plaintext password using PBKDF2-HMAC-SHA256 with a random salt.

    Args:
        password: Plaintext password to hash.

    Returns:
        Opaque string in the format
        ``pbkdf2_sha256$<iterations>$<salt_b64url>$<hash_b64url>``.
        Two calls with the same password produce different outputs.
    """
    # Pre:  password is a non-empty string
    # Post: returned string encodes algorithm, iterations, random salt,
    #       and derived key; never equal to password
    salt = secrets.token_bytes(_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac(_ALGORITHM, password.encode(), salt, _ITERATIONS)
    salt_b64 = base64.urlsafe_b64encode(salt).rstrip(b"=").decode()
    hash_b64 = base64.urlsafe_b64encode(dk).rstrip(b"=").decode()
    return (
        f"pbkdf2_{_ALGORITHM}"
        f"{_SEP}{_ITERATIONS}"
        f"{_SEP}{salt_b64}"
        f"{_SEP}{hash_b64}"
    )


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored PBKDF2-SHA256 hash.

    Args:
        password: Plaintext candidate password.
        hashed: Value previously returned by :func:`hash_password`.

    Returns:
        ``True`` if the password matches, ``False`` otherwise.
        Comparison is performed in constant time to prevent timing attacks.
    """
    # Pre:  hashed was produced by hash_password (format: algo$iters$salt$hash)
    # Post: returns True iff password matches; never raises on malformed input
    try:
        parts = hashed.split(_SEP)
        if len(parts) != 4:  # algo, iters, salt, hash
            return False
        _, iterations_str, salt_b64, stored_b64 = parts
        iterations = int(iterations_str)
        padding = "=" * (-len(salt_b64) % 4)
        salt = base64.urlsafe_b64decode(salt_b64 + padding)
    except ValueError:
        return False

    dk = hashlib.pbkdf2_hmac(_ALGORITHM, password.encode(), salt, iterations)
    candidate_b64 = base64.urlsafe_b64encode(dk).rstrip(b"=").decode()
    return hmac.compare_digest(candidate_b64, stored_b64)
