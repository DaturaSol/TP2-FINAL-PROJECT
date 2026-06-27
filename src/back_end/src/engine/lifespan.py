# ./src/back_end/src/engine/lifespan.py
"""Lifespan of the app, what it does when it starts up and dies."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI

from engine.database import create_all_tables, init_db_engine
from engine.logger import setup_logging
from engine.schemas.sql import CentralDeclarativeBase
from engine.settings import app_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """What app will perform when it is instanciated."""
    engine = None
    client_session = None
    # --- Startup ---
    try:
        # 0. Logging
        setup_logging()

        # 1. Database
        engine = init_db_engine(app_settings.database.url)
        app.state.db_engine = engine
        await create_all_tables(engine, CentralDeclarativeBase.metadata)

        # 2. Client Session
        client_session = ClientSession()
        app.state.client_session = client_session

        yield  # app returns here

    # --- Shutdown ---
    finally:
        # 1. Database
        if engine:
            await engine.dispose()

        # 2. Client Session
        if client_session and not client_session.closed:
            await client_session.close()
