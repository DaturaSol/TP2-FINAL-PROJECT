# ./src/back_end/tests/database/test_crud.py
"""Testing crud."""

from sqlalchemy import Connection, String, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from engine.database._crud import create_all_tables, drop_all_tables
from engine.database._session import init_db_engine
from engine.settings import Settings


class TempBase(DeclarativeBase):
    """."""

    pass


class TempTable(TempBase):
    """."""

    __tablename__ = "test_table"
    id: Mapped[str] = mapped_column(String, primary_key=True)


def get_tables(connection: Connection) -> list[str]:
    """."""
    return inspect(connection).get_table_names()


async def test_table_lifecycle(mock_settings: Settings):
    """Objective: Test if we are able to create tables and drop them."""
    engine = init_db_engine(mock_settings.database.url)
    try:
        await create_all_tables(engine, TempTable.metadata)

        async with engine.connect() as conn:
            tables = await conn.run_sync(get_tables)

        assert TempTable.__tablename__ in tables
    finally:
        await drop_all_tables(engine, TempTable.metadata)

        async with engine.connect() as conn:
            tables = await conn.run_sync(get_tables)

        assert TempTable.__tablename__ not in tables

        await engine.dispose()
