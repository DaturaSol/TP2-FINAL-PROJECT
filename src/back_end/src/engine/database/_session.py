# ./src/back_end/src/engine/database/_session.py
"""Starts up and generates sessions to use the database.

SQLite3 is not async, but since we might have multiple
calls from the frontend, i think going with a async setup is a
good idea, so i am setting this up to make our life easier.
relax you wont need to touch here that much.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def init_db_engine(db_url: str) -> AsyncEngine:
    """Starts up a async engine.

    One engine is used to control sessions.
    """
    return create_async_engine(db_url, echo=False)


def _create_async_session(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )


@asynccontextmanager
async def get_async_session(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Generator for async session.

    Each db call will generate a local asynchronous session.
    """
    local_async_session = _create_async_session(engine)
    async with local_async_session() as async_session:
        try:
            yield async_session
            await async_session.commit()
        except Exception as e:
            await async_session.rollback()
            raise e
        finally:
            await async_session.close()
