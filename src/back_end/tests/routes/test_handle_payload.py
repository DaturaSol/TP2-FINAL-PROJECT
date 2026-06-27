# ./src/back_end/tests/routes/test_handle_payload.py
"""Integration tests for POST /webhook.

HU01: 201 on success, 409 on duplicate e-mail, 422 on validation failure,
400 on unrecognisable payload shape.
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

# The frontend sends the password already SHA-256-hashed, so the payloads
# below carry a hex digest rather than a plaintext password.
_DIGEST = hashlib.sha256(b"a-strong-password").hexdigest()


@asynccontextmanager
async def _no_lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """No-op lifespan so tests control app.state manually."""
    yield


@pytest.fixture
async def client(
    mock_settings: Settings,
) -> AsyncGenerator[AsyncClient, None]:
    """ASGI test client backed by an isolated in-memory test database."""
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


def _payload(
    email: str,
    password: str,
    name: str | None = None,
) -> dict[str, object]:
    """Build a JSON-serialisable registration payload."""
    logging: dict[str, str] = {"email": email, "password": password}
    if name is not None:
        logging["name"] = name
    return {"object": "frontend_payload", "entry": [{"logging": logging}]}


async def test_register_success_returns_201(client: AsyncClient) -> None:
    """HU01 criterion 1: valid data returns 201 with user info."""
    resp = await client.post(
        "/webhook",
        json=_payload("alice@example.com", _DIGEST, "Alice"),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["object"] == "backend_payload"
    user = data["entry"][0]["user_basic_info"]
    assert user["email"] == "alice@example.com"
    assert user["name"] == "Alice"
    assert isinstance(user["id"], int)
    assert "password" not in user


async def test_register_duplicate_returns_409(client: AsyncClient) -> None:
    """HU01 criterion 2: duplicate e-mail returns 409."""
    body = _payload("bob@example.com", _DIGEST)
    await client.post("/webhook", json=body)
    resp = await client.post("/webhook", json=body)
    assert resp.status_code == 409


async def test_register_invalid_email_returns_422(
    client: AsyncClient,
) -> None:
    """HU01 criterion 3: invalid e-mail format returns 422."""
    resp = await client.post("/webhook", json=_payload("not-an-email", _DIGEST))
    assert resp.status_code == 422
    assert "detail" in resp.json()


async def test_register_non_hash_password_returns_422(
    client: AsyncClient,
) -> None:
    """HU01 criterion 3: a password that is not a SHA-256 digest returns 422."""
    resp = await client.post(
        "/webhook", json=_payload("carol@example.com", "plaintext-password")
    )
    assert resp.status_code == 422
    assert "detail" in resp.json()


async def test_no_logging_entry_returns_400(client: AsyncClient) -> None:
    """400 is returned when the payload has no recognisable entry type."""
    resp = await client.post(
        "/webhook",
        json={
            "object": "frontend_payload",
            "entry": [{"logging": None}],
        },
    )
    assert resp.status_code == 400
