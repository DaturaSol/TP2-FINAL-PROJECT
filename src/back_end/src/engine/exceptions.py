# ./src/back_end/src/engine/exceptions.py
"""Domain-level exceptions for the engine package.

HU01: EmailAlreadyExistsError and NoActionableEntryError are raised
during user registration.
HU02: InvalidCredentialsError is raised during login.
"""


class EmailAlreadyExistsError(Exception):
    """Raised when create_user targets an e-mail already in the database."""


class NoActionableEntryError(Exception):
    """Raised when a webhook payload carries no recognisable entry type."""


class InvalidCredentialsError(Exception):
    """Raised on login when the e-mail is unknown or the password is wrong.

    The same error covers both cases on purpose, so callers cannot use it to
    discover which e-mail addresses are registered.
    """
