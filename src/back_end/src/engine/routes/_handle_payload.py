# ./src/back_end/src/engine/routes/_handle_payload.py
"""Request post router.

Receives a POST on /webhook, validates the payload, dispatches to
handle_webhook synchronously, and maps domain exceptions to HTTP
status codes.
"""

import json

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine

from engine.exceptions import EmailAlreadyExistsError, NoActionableEntryError
from engine.schemas.ingoing import WebHookPayload
from engine.services import handle_webhook

handle_webhook_payload_bp = APIRouter()


@handle_webhook_payload_bp.post("/webhook", response_model=None)
async def handle_payload(request: Request) -> Response:
    """Handle POST requests on /webhook.

    Parses and validates the incoming payload, then dispatches to
    handle_webhook synchronously.

    Returns:
        201 with the BackEndRequest body on success.
        409 when the e-mail is already registered.
        422 when field validation fails (invalid e-mail, short password).
        400 when the payload has no recognisable entry type.
        500 on unexpected errors.
    """
    # Pre:  request carries a JSON body shaped as WebHookPayload
    # Post: returns a JSON response; never leaks raw exceptions to caller
    try:
        raw: bytes = await request.body()
        payload = WebHookPayload.model_validate_json(raw)
        app: FastAPI = request.app
        engine: AsyncEngine = app.state.db_engine
        # HU01: dispatch registration synchronously so the response
        #       reflects success or failure of the operation
        result = await handle_webhook(payload, engine)
        return JSONResponse(result.model_dump(by_alias=True), status_code=201)
    except ValidationError as exc:
        # exc.json() uses pydantic's own encoder, which serialises the
        # ValueError objects stored in error ctx — plain exc.errors() does not.
        detail = json.loads(exc.json())
        return JSONResponse(
            {"error": "Validation failed", "detail": detail},
            status_code=422,
        )
    except EmailAlreadyExistsError:
        return JSONResponse(
            {"error": "E-mail already registered."},
            status_code=409,
        )
    except NoActionableEntryError:
        return JSONResponse(
            {"error": "Payload contains no recognisable entry type."},
            status_code=400,
        )
    except Exception:
        return JSONResponse(
            {"error": "Internal server error."}, status_code=500
        )
