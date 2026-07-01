# src/back_end/src/engine/schemas/sql/__init__.py
"""Declarations of the database lives here."""

from ._base_model import CentralDeclarativeBase
from ._shopping_list import ItensDaLista, ListasCompras
from ._user import User

__all__ = ["CentralDeclarativeBase", "User"]
__all__ = ["CentralDeclarativeBase", "ItensDaLista"]
__all__ = ["CentralDeclarativeBase", "ListasCompras"]
