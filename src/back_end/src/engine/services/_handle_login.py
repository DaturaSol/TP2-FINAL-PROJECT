# ./src/back_end/src/engine/services/_handle_login.py
"""Login business logic.

HU02: authenticate a user against the stored password hash and mint a
signed session token.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from engine.database import get_async_session, get_user
from engine.exceptions import InvalidCredentialsError
from engine.schemas.ingoing import LoginRequest
from engine.schemas.outgoing import LoginResponse, UserBasicEntry
from engine.security import create_token, verify_password


async def handle_login(
    payload: LoginRequest,
    engine: AsyncEngine,
) -> LoginResponse:
    """Authenticate a user and return a session token plus basic info.

    Args:
        payload: Validated credentials (e-mail + SHA-256 password digest).
        engine: Active database engine.

    Returns:
        A LoginResponse carrying a signed token and the user's basic info.

    Raises:
        InvalidCredentialsError: If the e-mail is unknown or the password
            does not match. The same error is raised for both cases so the
            caller cannot tell which e-mails are registered.
    """
    # Pre:  payload is a validated LoginRequest
    # Post: returns LoginResponse on success; raises InvalidCredentialsError
    #       on unknown e-mail or wrong password
    async with get_async_session(engine) as session:
        user = await get_user(session, payload.email)

    # verify_password is constant-time; we still always run it only when the
    # user exists. The shared error message keeps the two failures opaque.
    if user is None or not verify_password(payload.password, user.passwd):
        raise InvalidCredentialsError("Invalid e-mail or password.")

    return LoginResponse(
        token=create_token(user.id),
        usuario=UserBasicEntry(id=user.id, name=user.name, email=user.email),
    )
