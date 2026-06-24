# ./src/back_end/tests/test_security.py
"""Direct tests for engine.security.

HU01: verifies that hash_password and verify_password meet the
cryptographic requirements for safe password storage.
"""

from engine.security import hash_password, verify_password


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
