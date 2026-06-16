# ./src/back_end/src/engine/client.py
"""Holds methods to send messages to our frontend."""

from aiohttp import ClientError, ClientSession, ClientTimeout, ContentTypeError

from engine.schemas.outgoing import BackEndRequest


async def post_request(
    session: ClientSession, payload: BackEndRequest, timeout: int = 10
) -> dict | None:
    """Sends a simple payload to the frontend.

    Yes, gotta be asynchronously.
    I was nice and did a bit of a scaffold for whoever wants to take this.
    d=====(￣▽￣*)b
    """
    raise NotImplementedError
    # TODO: Make this work, good luck (~￣▽￣)~.
    url = ""  # Not sure yet
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }  # Knowing the charset is kinda useful, not necessary, can be removed.

    json_data = payload.model_dump(exclude_none=True, by_alias=True)

    try:
        async with session.post(
            url,
            json=json_data,
            headers=headers,
            timeout=ClientTimeout(total=timeout),
        ) as resp:
            data: dict = await resp.json()

            # Error
            if resp.status >= 400 or "error" in data:
                err: dict = data.get("error", {})
                err_message = err.get("message", data)  # noqa: F841
                return data

            return data
    except (ClientError, ContentTypeError, TimeoutError) as e:
        raise e
