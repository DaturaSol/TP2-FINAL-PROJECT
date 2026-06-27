# ./src/back_end/tests/test_client.py
"""Tests for engine.client.post_request.

aiohttp is not actually hit; a tiny fake session stands in for it so the
test stays fast and offline. We check three things: the payload is sent
correctly, ``exclude_none`` drops empty fields, and transport errors
propagate to the caller.
"""

import pytest
from aiohttp import ClientError, ClientTimeout

from engine.client import post_request
from engine.schemas.outgoing import BackEndRequest, Entry, UserBasicEntry


class _FakeResponse:
    """Stands in for the async context manager aiohttp returns from post()."""

    def __init__(self, json_body: dict) -> None:
        """Store the body that json() should hand back."""
        self._json_body = json_body

    async def __aenter__(self) -> "_FakeResponse":
        """Enter the ``async with`` block and expose the response."""
        return self

    async def __aexit__(self, *_exc: object) -> bool:
        """Leave the block without suppressing exceptions."""
        return False

    async def json(self) -> dict:
        """Return the canned JSON body."""
        return self._json_body


class _FakeSession:
    """Captures the arguments of a single post() call for assertions."""

    def __init__(self, response: _FakeResponse) -> None:
        """Remember the response to return and prepare a capture slot."""
        self._response = response
        self.received: dict | None = None

    def post(
        self,
        url: str,
        *,
        json: dict,
        headers: dict,
        timeout: ClientTimeout,
    ) -> _FakeResponse:
        """Record the call and return the canned response."""
        self.received = {
            "url": url,
            "json": json,
            "headers": headers,
            "timeout": timeout,
        }
        return self._response


class _RaisingResponse:
    """A response whose context entry fails, mimicking a network error."""

    async def __aenter__(self) -> "_RaisingResponse":
        """Raise as if the connection could not be established."""
        raise ClientError("connection failed")

    async def __aexit__(self, *_exc: object) -> bool:
        """Never reached; present to satisfy the protocol."""
        return False


class _RaisingSession:
    """Session whose post() yields a response that fails on entry."""

    def post(self, *_args: object, **_kwargs: object) -> _RaisingResponse:
        """Return a response that raises when used."""
        return _RaisingResponse()


def _make_payload(name: str | None = "Alice") -> BackEndRequest:
    """Build a sample BackEndRequest to send."""
    return BackEndRequest(
        object_="backend_payload",
        entry=[
            Entry(
                user_basic_info=UserBasicEntry(
                    id=1, name=name, email="alice@example.com"
                )
            )
        ],
    )


async def test_post_request_sends_serialised_payload_and_returns_json() -> None:
    """post_request serialises the payload, posts it, and returns the body."""
    session = _FakeSession(_FakeResponse({"status": "ok"}))
    result = await post_request(session, "http://front/api", _make_payload())

    assert result == {"status": "ok"}
    assert session.received is not None
    assert session.received["url"] == "http://front/api"
    assert session.received["headers"]["Content-Type"] == (
        "application/json; charset=utf-8"
    )
    # by_alias=True emits "object" rather than the field name "object_".
    assert session.received["json"]["object"] == "backend_payload"
    assert session.received["timeout"].total == 10


async def test_post_request_excludes_none_fields() -> None:
    """Optional fields that are None are dropped from the sent JSON."""
    session = _FakeSession(_FakeResponse({}))
    await post_request(session, "http://front/api", _make_payload(name=None))

    assert session.received is not None
    user_info = session.received["json"]["entry"][0]["user_basic_info"]
    assert "name" not in user_info


async def test_post_request_propagates_client_error() -> None:
    """A transport error from aiohttp is propagated to the caller."""
    with pytest.raises(ClientError):
        await post_request(
            _RaisingSession(), "http://front/api", _make_payload()
        )
