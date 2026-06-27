# ./src/back_end/src/engine/routes/_handle_login.py
"""Login route.

Receives a POST on /login, validates the flat credentials body, dispatches
to handle_login, and maps failures to HTTP status codes. The response shape
matches what the frontend expects: ``{"token", "usuario"}`` on success and
``{"message"}`` on error.
"""

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine

from engine.exceptions import InvalidCredentialsError
from engine.schemas.ingoing import LoginRequest
from engine.services import handle_login

handle_login_bp = APIRouter()


@handle_login_bp.post("/login", response_model=None)
async def handle_login_request(request: Request) -> Response:
    """Handle POST requests on /login.

    Returns:
        200 with {"token", "usuario"} on success.
        401 with {"message"} when the e-mail or password is wrong.
        422 with {"message"} when the body is malformed.
        500 with {"message"} on unexpected errors.
    """
    # Pre:  request carries a JSON body shaped as LoginRequest
    # Post: returns a JSON response; never leaks raw exceptions to caller
    try:
        raw: bytes = await request.body()
        payload = LoginRequest.model_validate_json(raw)
        app: FastAPI = request.app
        engine: AsyncEngine = app.state.db_engine
        result = await handle_login(payload, engine)
        return JSONResponse(result.model_dump(), status_code=200)
    except ValidationError:
        # The frontend reads `error.response.data.message`, so login errors
        # use a "message" field (the /webhook route uses "error").
        return JSONResponse(
            {"message": "Invalid e-mail or password format."},
            status_code=422,
        )
    except InvalidCredentialsError:
        return JSONResponse(
            {"message": "E-mail ou senha inválidos."},
            status_code=401,
        )
    except Exception:
        return JSONResponse(
            {"message": "Internal server error."}, status_code=500
        )
