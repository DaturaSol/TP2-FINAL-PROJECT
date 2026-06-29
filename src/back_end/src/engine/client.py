# ./src/back_end/src/engine/client.py
"""Outbound HTTP helper for talking to other services.

NOTE: In this project the backend answers the frontend *directly* on the
``POST /webhook`` response (see ``routes/_handle_payload.py``), so it never
needs to open a second connection back to the frontend. This helper is kept
small and self-contained for any future "fire a payload at some URL" need
(e.g. notifying an external service); it is intentionally not part of the
registration flow.
"""

import logging

from aiohttp import ClientSession, ClientTimeout

from engine.schemas.outgoing import BackEndRequest

logger = logging.getLogger(__name__)


async def post_request(
    session: ClientSession,
    url: str,
    payload: BackEndRequest,
    timeout: int = 10,
) -> dict[str, object]:
    """Send a payload to ``url`` as JSON and return the parsed response.

    Args:
        session: A live aiohttp session (the app keeps one on
            ``app.state.client_session``; see ``engine/lifespan.py``).
        url: Absolute URL to POST to.
        payload: The response object to serialise and send.
        timeout: Total request timeout in seconds.

    Returns:
        The response body parsed from JSON.

    Raises:
        aiohttp.ClientError: On connection/HTTP transport errors.
        TimeoutError: If the request takes longer than ``timeout`` seconds.
    """
    # Pre:  session is an open ClientSession and url is a valid absolute URL
    # Post: returns the parsed JSON body, or propagates a transport error

    # Tell the server we are sending UTF-8 JSON. The charset is optional but
    # makes our intent explicit and avoids any ambiguity on the other side.
    headers = {"Content-Type": "application/json; charset=utf-8"}

    # by_alias=True   -> emit "object" (not "object_"), matching the schema.
    # exclude_none=True -> drop empty optional fields to keep the body small.
    json_data = payload.model_dump(exclude_none=True, by_alias=True)

    # ``async with`` guarantees the connection is released even on error.
    async with session.post(
        url,
        json=json_data,
        headers=headers,
        timeout=ClientTimeout(total=timeout),
    ) as resp:
        data: dict[str, object] = await resp.json()
        logger.info("Decoding JSON into a dictionary is working correctly.")
        return data
