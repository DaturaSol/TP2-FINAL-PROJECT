# src/back_end/src/engine/schemas/outgoing/__init__.py
"""Outgoing pydantic json schemas for user."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ._user_basic import UserBasicEntry


class Entry(BaseModel):
    """Basic entry to send."""

    user_basic_info: UserBasicEntry | None


class BackEndRequest(BaseModel):
    """Pydantic json schema to what we will be sending."""

    model_config = ConfigDict(populate_by_name=True)

    object_: Literal["backend_payload"] = Field(..., alias="object")
    entry: list[Entry]


class LoginResponse(BaseModel):
    """Body returned on a successful login.

    Field names match what the frontend reads from the response: a session
    ``token`` and the user's basic info under ``usuario``.
    """

    token: str
    usuario: UserBasicEntry


__all__ = ["BackEndRequest", "Entry", "LoginResponse", "UserBasicEntry"]
