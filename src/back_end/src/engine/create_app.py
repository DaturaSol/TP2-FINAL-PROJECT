# ./src/back_end/src/engine/create_app.py
"""Creates the app objecet."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from engine.lifespan import lifespan
from engine.routes import routers
import logging


logger = logging.getLogger(__name__)

def create_app(lifespan=lifespan) -> FastAPI:
    """Starts up the app and include its routes."""
    app = FastAPI(lifespan=lifespan)
    # Permite requisições do frontend (Vite)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        app.include_router(router)
    logger.INFO("APP created with success.")
    return app
