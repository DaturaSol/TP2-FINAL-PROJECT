# ./src/back_end/src/engine/schemas/ingoing/__init__.py
"""Ingoing pydantic schemas for responses."""

from typing import Literal

from pydantic import BaseModel, Field

from ._logging import LoggingEntry
from ._login import LoginRequest


class Entry(BaseModel):
    """Message information goes inside of here."""

    logging: LoggingEntry | None = None


class WebHookPayload(BaseModel):
    """Easy lazy way to deal with payloads.

    Anything that follows this shape as a json can be parsed and
    validated.
    """

    object_: Literal["frontend_payload"] = Field(..., alias="object")
    entry: list[Entry]


# NOTE: In python the closest thing we have to code protection is this.
__all__ = ["LoginRequest", "WebHookPayload"]
