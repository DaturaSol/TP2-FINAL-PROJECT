# ./src/back_end/src/engine/routes/_handle_payload.py
"""Request post router.

Really simple, get a post on /webhook, validate that message,
handle task on background.
"""

from typing import Annotated

from aiohttp import ClientSession
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    Request,
    Response,
)
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine

from engine.schemas.ingoing import WebHookPayload
from engine.services import handle_webhook

handle_webhook_payload_bp = APIRouter()


async def _get_client_session_dependancy(request: Request) -> ClientSession:
    app: FastAPI = request.app
    client_session = app.state.client_session
    return client_session


# NOTE: Here is where most of the logic will live
@handle_webhook_payload_bp.post("/webhook", response_model=None)
async def handle_payload(
    request: Request,
    background_tasks: BackgroundTasks,
    client_session: Annotated[
        ClientSession, Depends(_get_client_session_dependancy)
    ],
) -> Response:
    """Handle post requests on /webhook.

    Really simple, get a post on /webhook, validate that message,
    handle task on background.
    """
    try:
        raw: bytes = await request.body()
        payload = WebHookPayload.model_validate_json(raw)
        app: FastAPI = request.app
        engine: AsyncEngine = app.state.db_engine

        # NOTE: We are handeling in the background, but it is not necessary
        # we can just do await handle_webhook(...), and do all the logic here.
        # You choose (#~-_ゝ-)
        # TODO: Implement this properly.
        background_tasks.add_task(
            handle_webhook, payload, engine, client_session
        )

        # TODO: Take proper care of these responses...
        return JSONResponse({"status": "success"}, status_code=200)
    # Not good we dont want to return internal errors.
    except ValidationError:  # Validation Error on Pydantic parsing
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)
    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)
