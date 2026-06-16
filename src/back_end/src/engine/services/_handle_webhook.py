# TODO: comments here ?
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncEngine

from engine.schemas.ingoing import WebHookPayload


# NOTE: I said in routes that that one was the most important, but i think
# it is much cleaner to do most of the logic here.
# TODO: Handle the payload
def handle_webhook(
    payload: WebHookPayload, engine: AsyncEngine, client_session: ClientSession
) -> None:
    raise NotImplementedError
