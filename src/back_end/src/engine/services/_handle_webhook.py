# ./src/back_end/src/engine/services/_handle_webhook.py
"""Webhook business logic.

HU01: processes registration entries from the webhook payload and
returns a typed BackEndRequest response.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from engine.database import create_user, get_async_session
from engine.exceptions import NoActionableEntryError
from engine.schemas.ingoing import WebHookPayload
from engine.schemas.outgoing import BackEndRequest, Entry, UserBasicEntry


async def handle_webhook(
    payload: WebHookPayload,
    engine: AsyncEngine,
) -> BackEndRequest:
    """Process a validated webhook payload and perform the matching action.

    Args:
        payload: Validated ingoing payload from the frontend.
        engine: Active database engine.

    Returns:
        A BackEndRequest with the result of the performed action.

    Raises:
        NoActionableEntryError: When no recognisable entry type is found
            in the payload.
        EmailAlreadyExistsError: When a registration targets a duplicate
            e-mail address.
    """
    # Pre:  payload is a fully validated WebHookPayload (field validators
    #       on LoggingEntry have already run)
    # Post: returns BackEndRequest on success; EmailAlreadyExistsError
    #       propagates from create_user; NoActionableEntryError raised
    #       when no known entry type is present
    for entry in payload.entry:
        if entry.logging is not None:
            log = entry.logging
            async with get_async_session(engine) as session:
                # HU01: persist the new user account
                user = await create_user(
                    session,
                    email=log.email,
                    passwd=log.password,
                    name=log.name,
                )
            user_entry = UserBasicEntry(
                id=user.id,
                name=user.name,
                email=user.email,
            )
            return BackEndRequest(
                object_="backend_payload",
                entry=[Entry(user_basic_info=user_entry)],
            )

    raise NoActionableEntryError(
        "Payload contained no recognisable entry type."
    )
