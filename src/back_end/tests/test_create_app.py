# ./src/back_end/tests/test_create_app.py
"""Tests for the create_app application factory.

Verifies the app is assembled correctly: it is a FastAPI instance, the
/webhook route is registered, and CORS is configured for the Vite frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from engine.create_app import create_app


def test_create_app_returns_fastapi_instance() -> None:
    """create_app builds and returns a FastAPI application."""
    app = create_app()
    assert isinstance(app, FastAPI)


def test_webhook_route_is_registered() -> None:
    """The POST /webhook route is included on the app."""
    app = create_app()
    # Read the OpenAPI schema rather than walking app.routes: this FastAPI
    # version keeps included routers nested, so their paths are not flattened
    # onto app.routes, but they always show up in the generated schema.
    paths = app.openapi()["paths"]
    assert "/webhook" in paths
    assert "post" in paths["/webhook"]


def test_login_route_is_registered() -> None:
    """The POST /login route is included on the app."""
    app = create_app()
    paths = app.openapi()["paths"]
    assert "/login" in paths
    assert "post" in paths["/login"]


def test_cors_middleware_is_configured() -> None:
    """CORS middleware is installed so the Vite frontend can call the API."""
    app = create_app()
    middleware_classes = [m.cls for m in app.user_middleware]
    assert CORSMiddleware in middleware_classes
