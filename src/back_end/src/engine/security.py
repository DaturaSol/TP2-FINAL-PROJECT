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
HU02: create_token / verify_token issue and check login session tokens.
"""

import base64
import hashlib
import hmac
import json
import logging
import secrets
import time

from engine.settings import app_settings

logger = logging.getLogger(__name__)

_ALGORITHM = "sha256"
_ITERATIONS = 600_000  # OWASP 2023 minimum for PBKDF2-HMAC-SHA256
_SALT_BYTES = 16
_SEP = "$"

_TOKEN_SEP = "."


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
            logger.warning(
                f"Malformed password hash verification attempt: {hashed} "
            )
            return False
        _, iterations_str, salt_b64, stored_b64 = parts
        iterations = int(iterations_str)
        padding = "=" * (-len(salt_b64) % 4)
        salt = base64.urlsafe_b64decode(salt_b64 + padding)

    except ValueError:
        logger.error(f"ValueError when decoding hash: {hashed}")
        return False

    dk = hashlib.pbkdf2_hmac(_ALGORITHM, password.encode(), salt, iterations)
    candidate_b64 = base64.urlsafe_b64encode(dk).rstrip(b"=").decode()
    return hmac.compare_digest(candidate_b64, stored_b64)


def _b64(raw: bytes) -> str:
    """URL-safe base64 without padding (compact and URL-friendly)."""
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _token_secret() -> bytes:
    """Return the configured signing secret as bytes.

    Read at call time so a settings override (env / tests) is honoured.
    """
    return app_settings.security.secret_key.encode()


def create_token(user_id: int) -> str:
    """Create a signed session token for an authenticated user.

    The token is ``<payload>.<signature>`` where payload is a base64url JSON
    object ``{"uid": <id>, "iat": <unix-seconds>}`` and signature is an
    HMAC-SHA256 of that payload signed with the configured secret. It is not
    encrypted — the payload is readable — but it cannot be forged without the
    secret, which is what lets :func:`verify_token` trust it later.

    Args:
        user_id: Primary key of the authenticated user.

    Returns:
        An opaque, URL-safe token string.
    """
    # Pre:  user_id identifies an existing user
    # Post: returns a token that verify_token maps back to user_id
    payload = {"uid": user_id, "iat": int(time.time())}
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    payload_b64 = _b64(payload_json.encode())
    signature = hmac.new(
        _token_secret(), payload_b64.encode(), hashlib.sha256
    ).digest()
    return f"{payload_b64}{_TOKEN_SEP}{_b64(signature)}"


def verify_token(token: str) -> int | None:
    """Verify a token from :func:`create_token` and return its user id.

    Args:
        token: An arbitrary, possibly hostile token string.

    Returns:
        The user id encoded in the token, or ``None`` if the token is
        malformed or its signature does not match. Never raises.
    """
    # Pre:  token is any string
    # Post: returns the encoded user id iff the signature is valid, else None
    parts = token.split(_TOKEN_SEP)
    if len(parts) != 2:
        return None
    payload_b64, signature_b64 = parts

    expected = hmac.new(
        _token_secret(), payload_b64.encode(), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(_b64(expected), signature_b64):
        return None

    try:
        padding = "=" * (-len(payload_b64) % 4)
        decoded = base64.urlsafe_b64decode(payload_b64 + padding)
        payload = json.loads(decoded)
    except ValueError:
        return None
    if not isinstance(payload, dict):
        return None

    uid = payload.get("uid")
    # bool is a subclass of int; reject it so True can't pose as user id 1.
    return uid if isinstance(uid, int) and not isinstance(uid, bool) else None
