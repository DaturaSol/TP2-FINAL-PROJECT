# ./src/back_end/src/engine/exceptions.py
"""Domain-level exceptions for the engine package.

HU01: EmailAlreadyExistsError and NoActionableEntryError are raised
during user registration.
"""


class EmailAlreadyExistsError(Exception):
    """Raised when create_user targets an e-mail already in the database."""


class NoActionableEntryError(Exception):
    """Raised when a webhook payload carries no recognisable entry type."""
