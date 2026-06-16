# src/back_end/src/engine/schemas/sql/_base_model.py
"""Declarative base, of which other models must inherit.

Every model inherited from this class will be saved as metadata.
"""

from sqlalchemy.orm import DeclarativeBase


# NOTE: Please dont touch this.
class CentralDeclarativeBase(DeclarativeBase):
    """Central Metadata Registry.

    All models in the app must inherit from THIS class.
    """

    pass
