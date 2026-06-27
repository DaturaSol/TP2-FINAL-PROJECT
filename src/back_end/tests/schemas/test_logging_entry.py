# ./src/back_end/tests/schemas/test_logging_entry.py
"""Unit tests for LoggingEntry field validators.

HU01: covers criterion 3 (validation errors on invalid input fields).

Since the frontend now sends the password already hashed with SHA-256, the
``password`` field is validated as a 64-character hex digest.
"""

import hashlib

import pytest
from pydantic import ValidationError

from engine.schemas.ingoing._logging import LoggingEntry

# A realistic, valid SHA-256 hex digest (what the frontend would send).
_DIGEST = hashlib.sha256(b"correct horse battery staple").hexdigest()


def test_valid_entry_is_accepted() -> None:
    """A well-formed entry (valid e-mail + SHA-256 digest) is accepted."""
    entry = LoggingEntry(email="user@example.com", password=_DIGEST)
    assert entry.email == "user@example.com"
    assert entry.password == _DIGEST


def test_email_is_stripped_and_lowercased() -> None:
    """HU01: e-mail is normalised so duplicate-check is case-insensitive."""
    entry = LoggingEntry(email="  USER@EXAMPLE.COM  ", password=_DIGEST)
    assert entry.email == "user@example.com"


def test_invalid_email_raises_validation_error() -> None:
    """HU01 criterion 3: invalid e-mail format raises ValidationError."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="not-an-email", password=_DIGEST)


def test_missing_at_sign_raises_validation_error() -> None:
    """HU01 criterion 3: e-mail without @ raises ValidationError."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="userexample.com", password=_DIGEST)


def test_valid_sha256_digest_is_accepted() -> None:
    """A 64-character lowercase hex digest is accepted as the password."""
    entry = LoggingEntry(email="user@example.com", password=_DIGEST)
    assert len(entry.password) == 64


def test_uppercase_digest_is_normalised_to_lowercase() -> None:
    """An uppercase hex digest is accepted and stored lowercased."""
    entry = LoggingEntry(email="user@example.com", password=_DIGEST.upper())
    assert entry.password == _DIGEST


def test_surrounding_whitespace_is_stripped() -> None:
    """Whitespace around the digest is trimmed before validation."""
    entry = LoggingEntry(email="user@example.com", password=f"  {_DIGEST}  ")
    assert entry.password == _DIGEST


def test_non_hash_password_raises_validation_error() -> None:
    """HU01 criterion 3: a plaintext (non-digest) password is rejected."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="user@example.com", password="not-a-hash")


def test_wrong_length_digest_raises_validation_error() -> None:
    """A hex string that is not exactly 64 characters is rejected."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="user@example.com", password="abc123")  # too short
    with pytest.raises(ValidationError):
        LoggingEntry(email="user@example.com", password=_DIGEST + "ab")  # long


def test_non_hex_characters_raise_validation_error() -> None:
    """A 64-character string with non-hex characters is rejected."""
    not_hex = "z" * 64
    with pytest.raises(ValidationError):
        LoggingEntry(email="user@example.com", password=not_hex)


def test_name_defaults_to_none() -> None:
    """Name is optional and defaults to None when omitted."""
    entry = LoggingEntry(email="user@example.com", password=_DIGEST)
    assert entry.name is None


def test_name_is_accepted_when_provided() -> None:
    """Name is stored as-is when provided."""
    entry = LoggingEntry(
        email="user@example.com", password=_DIGEST, name="Alice"
    )
    assert entry.name == "Alice"
