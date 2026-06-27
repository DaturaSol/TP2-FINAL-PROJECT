# ./src/back_end/tests/routes/test_handle_login.py
"""Integration tests for POST /login.

HU02: 200 with token + usuario on valid credentials, 401 on bad
credentials (unknown e-mail or wrong password), 422 on a malformed body.
"""

import hashlib
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from engine.create_app import create_app
from engine.database import create_all_tables, init_db_engine
from engine.database._crud import drop_all_tables
from engine.schemas.sql import CentralDeclarativeBase
from engine.settings import Settings

# The digest the frontend sends for the correct password.
_DIGEST = hashlib.sha256(b"login-password").hexdigest()


@asynccontextmanager
async def _no_lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """No-op lifespan so tests control app.state manually."""
    yield


@pytest.fixture
async def client(
    mock_settings: Settings,
) -> AsyncGenerator[AsyncClient, None]:
    """ASGI test client backed by an isolated test database."""
    app = create_app(lifespan=_no_lifespan)
    engine = init_db_engine(mock_settings.database.url)
    await create_all_tables(engine, CentralDeclarativeBase.metadata)
    app.state.db_engine = engine
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    await drop_all_tables(engine, CentralDeclarativeBase.metadata)
    await engine.dispose()


async def _register(client: AsyncClient, email: str, password: str) -> None:
    """Register a user through /webhook so /login has someone to find."""
    await client.post(
        "/webhook",
        json={
            "object": "frontend_payload",
            "entry": [
                {"logging": {"name": "U", "email": email, "password": password}}
            ],
        },
    )


async def test_login_success_returns_200(client: AsyncClient) -> None:
    """Valid credentials return 200 with a token and usuario info."""
    await _register(client, "ok@example.com", _DIGEST)
    resp = await client.post(
        "/login", json={"email": "ok@example.com", "password": _DIGEST}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token"]
    assert data["usuario"]["email"] == "ok@example.com"
    assert "password" not in data["usuario"]


async def test_login_wrong_password_returns_401(client: AsyncClient) -> None:
    """A wrong password returns 401 with a message field."""
    await _register(client, "wp@example.com", _DIGEST)
    wrong = hashlib.sha256(b"nope").hexdigest()
    resp = await client.post(
        "/login", json={"email": "wp@example.com", "password": wrong}
    )
    assert resp.status_code == 401
    assert "message" in resp.json()


async def test_login_unknown_email_returns_401(client: AsyncClient) -> None:
    """An unknown e-mail returns 401 (same as a wrong password)."""
    resp = await client.post(
        "/login", json={"email": "ghost@example.com", "password": _DIGEST}
    )
    assert resp.status_code == 401


async def test_login_malformed_body_returns_422(client: AsyncClient) -> None:
    """A malformed body (bad e-mail / non-digest password) returns 422."""
    resp = await client.post(
        "/login", json={"email": "not-an-email", "password": "plaintext"}
    )
    assert resp.status_code == 422
    assert "message" in resp.json()
