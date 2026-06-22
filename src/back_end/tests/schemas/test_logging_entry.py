# ./src/back_end/tests/schemas/test_logging_entry.py
"""Unit tests for LoggingEntry field validators.

HU01: covers criterion 3 (validation errors on invalid input fields).
"""

import pytest
from pydantic import ValidationError

from engine.schemas.ingoing._logging import LoggingEntry


def test_valid_entry_is_accepted() -> None:
    """A well-formed entry is accepted without error."""
    entry = LoggingEntry(email="user@example.com", password="12345678")
    assert entry.email == "user@example.com"
    assert entry.password == "12345678"


def test_email_is_stripped_and_lowercased() -> None:
    """HU01: e-mail is normalised so duplicate-check is case-insensitive."""
    entry = LoggingEntry(email="  USER@EXAMPLE.COM  ", password="12345678")
    assert entry.email == "user@example.com"


def test_invalid_email_raises_validation_error() -> None:
    """HU01 criterion 3: invalid e-mail format raises ValidationError."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="not-an-email", password="12345678")


def test_missing_at_sign_raises_validation_error() -> None:
    """HU01 criterion 3: e-mail without @ raises ValidationError."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="userexample.com", password="12345678")


def test_short_password_raises_validation_error() -> None:
    """HU01 criterion 3: password under 8 chars raises ValidationError."""
    with pytest.raises(ValidationError):
        LoggingEntry(email="user@example.com", password="short")


def test_exactly_minimum_password_length_is_accepted() -> None:
    """Password of exactly 8 characters is accepted."""
    entry = LoggingEntry(email="user@example.com", password="12345678")
    assert len(entry.password) == 8


def test_name_defaults_to_none() -> None:
    """Name is optional and defaults to None when omitted."""
    entry = LoggingEntry(email="user@example.com", password="12345678")
    assert entry.name is None


def test_name_is_accepted_when_provided() -> None:
    """Name is stored as-is when provided."""
    entry = LoggingEntry(
        email="user@example.com", password="12345678", name="Alice"
    )
    assert entry.name == "Alice"
