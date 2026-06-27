# ./src/back_end/tests/services/test_handle_webhook.py
"""Tests for the handle_webhook service.

HU01: happy path and duplicate e-mail scenarios at the service layer.
"""

import hashlib

import pytest

from engine.database import create_all_tables, init_db_engine
from engine.database._crud import drop_all_tables
from engine.exceptions import EmailAlreadyExistsError, NoActionableEntryError
from engine.schemas.ingoing import WebHookPayload
from engine.schemas.sql import CentralDeclarativeBase
from engine.services import handle_webhook
from engine.settings import Settings

# The frontend sends the password already SHA-256-hashed.
_DIGEST = hashlib.sha256(b"service-layer-password").hexdigest()


def _make_payload(
    email: str,
    password: str,
    name: str | None = None,
) -> WebHookPayload:
    """Build a minimal registration WebHookPayload."""
    logging_data: dict[str, str] = {"email": email, "password": password}
    if name is not None:
        logging_data["name"] = name
    return WebHookPayload.model_validate(
        {
            "object": "frontend_payload",
            "entry": [{"logging": logging_data}],
        }
    )


async def test_handle_webhook_success(mock_settings: Settings) -> None:
    """HU01 criterion 1: valid payload returns BackEndRequest with user data."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        payload = _make_payload("hw@example.com", _DIGEST, "HW User")
        result = await handle_webhook(payload, engine)
        assert len(result.entry) == 1
        info = result.entry[0].user_basic_info
        assert info is not None
        assert info.email == "hw@example.com"
        assert info.name == "HW User"
        assert info.id > 0
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_handle_webhook_duplicate_raises(
    mock_settings: Settings,
) -> None:
    """HU01 criterion 2: duplicate e-mail raises EmailAlreadyExistsError."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        payload = _make_payload("dup@example.com", _DIGEST)
        await handle_webhook(payload, engine)
        with pytest.raises(EmailAlreadyExistsError):
            await handle_webhook(payload, engine)
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_handle_webhook_no_entry_raises(
    mock_settings: Settings,
) -> None:
    """NoActionableEntryError is raised when no logging entry is present."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        empty_payload = WebHookPayload.model_validate(
            {"object": "frontend_payload", "entry": [{"logging": None}]}
        )
        with pytest.raises(NoActionableEntryError):
            await handle_webhook(empty_payload, engine)
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()
