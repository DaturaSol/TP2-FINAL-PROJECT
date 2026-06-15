# ./src/back_end/tests/test_settings.py
"""Test unit for settings."""

from engine.settings import Settings


def test_settings_values(mock_settings: Settings) -> None:
    """Check if default values are being parsed and mocked correctly."""
    assert mock_settings.database.url == "sqlite+aiosqlite:///./test_mock.db"
