# ./src/back_end/tests/conftest.py
"""Basic mock settings used here, more organized than kept on differet files."""

import pytest

from engine.settings import Settings


@pytest.fixture(autouse=True)
def mock_settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """Automatically mock the settings for all tests.

    autouse=True ensures no test accidentally connects to the real database.
    """
    monkeypatch.setenv("DATABASE__URL", "sqlite+aiosqlite:///./test_mock.db")

    mocked_settings = Settings()
    monkeypatch.setattr("engine.settings.app_settings", mocked_settings)

    return mocked_settings
