# ./src/back_end/tests/database/test_user.py
"""Tests for engine.database._user (create_user and get_user).

HU01: covers the three acceptance criteria at the data layer:
  1. Valid data -> user created successfully.
  2. Duplicate e-mail -> EmailAlreadyExistsError raised.
  3. Password stored hashed and verifiable via verify_password.
"""

from datetime import datetime

import pytest

from engine.database import (
    create_all_tables,
    create_user,
    get_async_session,
    get_user,
    init_db_engine,
)
from engine.database._crud import drop_all_tables
from engine.exceptions import EmailAlreadyExistsError
from engine.schemas.sql import CentralDeclarativeBase
from engine.security import verify_password
from engine.settings import Settings


async def test_create_user_success(mock_settings: Settings) -> None:
    """HU01 criterion 1: valid data creates a user and returns it."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        async with get_async_session(engine) as session:
            user = await create_user(
                session, "alice@example.com", "securepass1", "Alice"
            )
        assert user.id is not None
        assert user.email == "alice@example.com"
        assert user.name == "Alice"
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_create_user_password_is_hashed(
    mock_settings: Settings,
) -> None:
    """HU01 criterion 3: password is stored hashed; verify_password confirms."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        plaintext = "my-plaintext-password"
        async with get_async_session(engine) as session:
            user = await create_user(session, "bob@example.com", plaintext)
        assert user.passwd != plaintext
        assert verify_password(plaintext, user.passwd) is True
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_create_user_duplicate_email_raises(
    mock_settings: Settings,
) -> None:
    """HU01 criterion 2: duplicate e-mail must raise EmailAlreadyExistsError."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        async with get_async_session(engine) as session:
            await create_user(session, "carol@example.com", "pass1")

        with pytest.raises(EmailAlreadyExistsError):
            async with get_async_session(engine) as session:
                await create_user(session, "carol@example.com", "pass2")
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_get_user_returns_existing(mock_settings: Settings) -> None:
    """get_user returns the row for a known e-mail."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        async with get_async_session(engine) as session:
            await create_user(session, "dave@example.com", "pass")
        async with get_async_session(engine) as session:
            found = await get_user(session, "dave@example.com")
        assert found is not None
        assert found.email == "dave@example.com"
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_get_user_returns_none_for_missing(
    mock_settings: Settings,
) -> None:
    """get_user returns None when the e-mail is not in the database."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        async with get_async_session(engine) as session:
            found = await get_user(session, "nobody@example.com")
        assert found is None
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()


async def test_create_user_persists_optional_fields(
    mock_settings: Settings,
) -> None:
    """Optional name and birthday are stored and read back unchanged."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, CentralDeclarativeBase.metadata)
        birthday = datetime(1990, 5, 17)
        async with get_async_session(engine) as session:
            await create_user(
                session,
                "eve@example.com",
                "pass",
                name="Eve",
                birthday=birthday,
            )
        async with get_async_session(engine) as session:
            found = await get_user(session, "eve@example.com")
        assert found is not None
        assert found.name == "Eve"
        assert found.birthday == birthday
    finally:
        await drop_all_tables(engine, CentralDeclarativeBase.metadata)
        await engine.dispose()
