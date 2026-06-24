# ./src/back_end/src/engine/create_app.py
"""Creates the app objecet."""

from fastapi import FastAPI

from engine.lifespan import lifespan
from engine.routes import routers


# TODO: test this
def create_app(lifespan=lifespan) -> FastAPI:
    """Starts up the app and include its routes."""
    app = FastAPI(lifespan=lifespan)
    for router in routers:
        app.include_router(router)
    return app
