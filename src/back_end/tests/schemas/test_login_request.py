# ./src/back_end/tests/schemas/test_login_request.py
"""Unit tests for the LoginRequest schema.

HU02: the login body carries an e-mail and a SHA-256 password digest, with
the same validation rules as registration.
"""

import hashlib

import pytest
from pydantic import ValidationError

from engine.schemas.ingoing import LoginRequest

_DIGEST = hashlib.sha256(b"a-password").hexdigest()


def test_valid_login_request_is_accepted() -> None:
    """A valid e-mail plus SHA-256 digest is accepted."""
    req = LoginRequest(email="user@example.com", password=_DIGEST)
    assert req.email == "user@example.com"
    assert req.password == _DIGEST


def test_email_is_normalised() -> None:
    """E-mail is stripped and lowercased, matching registration."""
    req = LoginRequest(email="  USER@EXAMPLE.COM  ", password=_DIGEST)
    assert req.email == "user@example.com"


def test_uppercase_digest_is_normalised() -> None:
    """An uppercase digest is accepted and stored lowercased."""
    req = LoginRequest(email="user@example.com", password=_DIGEST.upper())
    assert req.password == _DIGEST


def test_invalid_email_raises() -> None:
    """An invalid e-mail raises ValidationError."""
    with pytest.raises(ValidationError):
        LoginRequest(email="not-an-email", password=_DIGEST)


def test_non_digest_password_raises() -> None:
    """A plaintext (non-digest) password raises ValidationError."""
    with pytest.raises(ValidationError):
        LoginRequest(email="user@example.com", password="plaintext")
