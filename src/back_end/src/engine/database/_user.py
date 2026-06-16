# ./src/back_end/database/_user.py
"""User basic methods."""

# TODO: Add testing for this, comment and other complementary methods
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from engine.schemas.sql import User


# TODO: Missing other functions ??
async def create_user(
    session: AsyncSession,
    email: str,
    passwd: str,
    name: str | None = None,
    birthday: datetime | None = None,
) -> User:
    """Creates an user."""
    new_user = User(
        email=email,
        passwd=passwd,
        name=name,
        birthday=birthday,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def get_user(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)

    return result.scalar_one_or_none()
