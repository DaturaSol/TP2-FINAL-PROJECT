# ./src/back_end/tests/services/test_handle_login.py
"""Tests for the handle_login service.

HU02: success returns a verifiable token + user info; unknown e-mail and
wrong password both raise InvalidCredentialsError.
"""

import hashlib

import pytest

from engine.database import (
    create_all_tables,
    create_user,
    get_async_session,
    init_db_engine,
)
from engine.database._crud import drop_all_tables
from engine.exceptions import InvalidCredentialsError
from engine.schemas.ingoing import LoginRequest
from engine.schemas.sql import CentralDeclarativeBase
from engine.security import verify_token
from engine.services import handle_login
from engine.settings import Settings

# The digest the frontend would send for the correct password.
_DIGEST = hashlib.sha256(b"correct-password").hexdigest()


async def test_handle_login_success(mock_settings: Settings) -> None:
    """Valid credentials return a token (verifiable to the user id) + info."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        async with get_async_session(engine) as session:
            user = await create_user(
                session, "login@example.com", _DIGEST, "Login User"
            )

        payload = LoginRequest(email="login@example.com", password=_DIGEST)
        result = await handle_login(payload, engine)

        assert result.usuario.id == user.id
        assert result.usuario.email == "login@example.com"
        assert result.usuario.name == "Login User"
        assert verify_token(result.token) == user.id
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_handle_login_wrong_password_raises(
    mock_settings: Settings,
) -> None:
    """A wrong password raises InvalidCredentialsError."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        async with get_async_session(engine) as session:
            await create_user(session, "wp@example.com", _DIGEST)

        wrong = hashlib.sha256(b"wrong-password").hexdigest()
        payload = LoginRequest(email="wp@example.com", password=wrong)
        with pytest.raises(InvalidCredentialsError):
            await handle_login(payload, engine)
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_handle_login_unknown_email_raises(
    mock_settings: Settings,
) -> None:
    """An unknown e-mail raises InvalidCredentialsError (no enumeration)."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        payload = LoginRequest(email="ghost@example.com", password=_DIGEST)
        with pytest.raises(InvalidCredentialsError):
            await handle_login(payload, engine)
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()
