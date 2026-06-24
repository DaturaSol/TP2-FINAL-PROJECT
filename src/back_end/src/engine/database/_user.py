# ./src/back_end/src/engine/database/_user.py
"""User database operations.

HU01: create_user and get_user implement the data-layer contract for
user registration (criteria 1-3).
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from engine.exceptions import EmailAlreadyExistsError
from engine.schemas.sql import User
from engine.security import hash_password


async def create_user(
    session: AsyncSession,
    email: str,
    passwd: str,
    name: str | None = None,
    birthday: datetime | None = None,
) -> User:
    """Create and persist a new user with a hashed password.

    Args:
        session: Active database session.
        email: User's e-mail address (must be unique in the database).
        passwd: Plaintext password; stored as a PBKDF2-SHA256 hash.
        name: Optional display name.
        birthday: Optional date of birth.

    Returns:
        The newly created and refreshed User row.

    Raises:
        EmailAlreadyExistsError: If the e-mail is already registered.
    """
    # Pre:  session is an active AsyncSession; email and passwd are non-empty
    # Post: User is persisted with passwd hashed (never stored in plaintext);
    #       raises EmailAlreadyExistsError on duplicate email and leaves the
    #       session in a clean state after rollback
    new_user = User(
        email=email,
        passwd=hash_password(passwd),
        name=name,
        birthday=birthday,
    )
    session.add(new_user)
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        raise EmailAlreadyExistsError(email) from None
    await session.refresh(new_user)
    return new_user


async def get_user(session: AsyncSession, email: str) -> User | None:
    """Retrieve a user row by e-mail address.

    Args:
        session: Active database session.
        email: E-mail address to look up.

    Returns:
        The matching User row, or ``None`` if not found.
    """
    # Pre:  session is active
    # Post: returns the User row for email, or None if absent
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
