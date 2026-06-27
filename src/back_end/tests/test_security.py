# ./src/back_end/tests/test_security.py
"""Direct tests for engine.security.

HU01: verifies that hash_password and verify_password meet the
cryptographic requirements for safe password storage.
HU02: verifies create_token / verify_token round-trip and reject forgery.
"""

import base64
import json

from engine.security import (
    _b64,
    _token_secret,
    create_token,
    hash_password,
    verify_password,
    verify_token,
)


def _sign(payload_b64: str) -> str:
    """Build a validly-signed token over an arbitrary base64 payload.

    Used to exercise verify_token's defensive branches: a correct signature
    over a payload that is not the JSON object create_token would produce.
    """
    import hashlib
    import hmac

    signature = hmac.new(
        _token_secret(), payload_b64.encode(), hashlib.sha256
    ).digest()
    return f"{payload_b64}.{_b64(signature)}"


def test_hash_produces_different_outputs_for_same_password() -> None:
    """Two hashes of the same password must differ (random salt)."""
    h1 = hash_password("same-password")
    h2 = hash_password("same-password")
    assert h1 != h2


def test_verify_password_correct() -> None:
    """verify_password must return True for the original password."""
    hashed = hash_password("correct-password")
    assert verify_password("correct-password", hashed) is True


def test_verify_password_wrong() -> None:
    """verify_password must return False for a different password."""
    hashed = hash_password("correct-password")
    assert verify_password("wrong-password", hashed) is False


def test_round_trip() -> None:
    """hash_password followed by verify_password must confirm the password."""
    password = "round-trip-secret-123!"
    assert verify_password(password, hash_password(password)) is True


def test_verify_password_malformed_hash() -> None:
    """verify_password must return False for garbage input, not raise."""
    # wrong number of segments -> length check branch
    assert verify_password("any", "not-a-valid-hash") is False
    assert verify_password("any", "") is False
    assert verify_password("any", "$$$$$") is False
    # four segments but non-integer iteration count -> ValueError branch
    assert verify_password("any", "pbkdf2_sha256$NaN$salt$hash") is False


def test_token_round_trip() -> None:
    """create_token then verify_token returns the original user id."""
    token = create_token(42)
    assert verify_token(token) == 42


def test_verify_token_rejects_tampered_signature() -> None:
    """A token whose signature is altered is rejected."""
    payload_b64, _signature = create_token(7).split(".")
    assert verify_token(f"{payload_b64}.AAAA") is None


def test_verify_token_rejects_forged_payload() -> None:
    """Swapping in a different payload invalidates the original signature."""
    _payload, signature_b64 = create_token(7).split(".")
    forged = (
        base64.urlsafe_b64encode(json.dumps({"uid": 999, "iat": 0}).encode())
        .rstrip(b"=")
        .decode()
    )
    assert verify_token(f"{forged}.{signature_b64}") is None


def test_verify_token_rejects_garbage() -> None:
    """Malformed tokens return None instead of raising."""
    assert verify_token("") is None
    assert verify_token("not-a-token") is None
    assert verify_token("a.b.c") is None


def test_verify_token_rejects_signed_non_decodable_payload() -> None:
    """A correctly signed but non-JSON payload returns None, never raises."""
    assert verify_token(_sign(_b64(b"\xff\xfenot json"))) is None


def test_verify_token_rejects_signed_non_object_payload() -> None:
    """A correctly signed JSON value that is not an object returns None."""
    assert verify_token(_sign(_b64(b"5"))) is None  # JSON int, not a dict
