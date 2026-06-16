# ./src/back_end/tests/database/test_session.py
"""Tests async session."""

from sqlalchemy import text

from engine.database.session import init_db_engine
from engine.settings import Settings


async def test_database_connection(mock_settings: Settings):
    """Objective: Connect to the Database."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
    finally:
        await engine.dispose()

    assert value == 1
