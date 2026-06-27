# src/back_end/src/engine/schemas/sql/_user.py
"""User database declaration.

Wired into the request flow via ``database.create_user`` (called from the
``handle_webhook`` service, which the ``POST /webhook`` route dispatches to).
Exercised by the tests under tests/database/ and tests/routes/.
"""

import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ._base_model import CentralDeclarativeBase


class User(CentralDeclarativeBase):
    """User sql table declaration.

    Already inherits from Central Base.
    """

    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    passwd: Mapped[str] = mapped_column(String(128))
    name: Mapped[str | None] = mapped_column(String(50))
    birthday: Mapped[datetime.datetime | None] = mapped_column(DateTime)

    def __init__(
        self,
        email: str,
        passwd: str,
        name: str | None = None,
        birthday: datetime.datetime | None = None,
    ):
        super().__init__()
        self.email = email
        self.passwd = passwd
        self.name = name
        self.birthday = birthday
