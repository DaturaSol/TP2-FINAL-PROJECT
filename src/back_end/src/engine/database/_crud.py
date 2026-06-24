# ./src/back_end/src/engine/database/_crud.py
"""Basic set of methods for the database."""

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine


async def create_all_tables(engine: AsyncEngine, metadata: MetaData) -> None:
    """Run only once when startying the app."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def drop_all_tables(engine: AsyncEngine, metadata: MetaData) -> None:
    """Dangerous function, why is here?

    Makes testing easier ƪ(˘⌣˘)ʃ
    """
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
