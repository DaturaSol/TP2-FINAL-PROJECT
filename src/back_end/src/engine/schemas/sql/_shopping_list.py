# src/back_end/src/engine/schemas/sql/_shopping_list.py
"""Banco de dados da lista de compras.

Criação do banco para as listas de compras e os itens da lista.
"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ._base_model import CentralDeclarativeBase


class ListaStatus(Enum):
    """Status da lista de compras."""

    ATIVA = "ativa"
    FINALIZADA = "finalizada"
    ARQUIVADA = "arquivada"


class ListasCompras(CentralDeclarativeBase):
    """Modelo ORM para a tabela de listas de compras."""

    __tablename__ = "listas_de_compras"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    data_de_criacao_da_lista: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[ListaStatus] = mapped_column(
        Enum("ListaStatus"), default=ListaStatus.ATIVA, nullable=False
    )

    # relacionamento
    itens: Mapped[list["ItensDaLista"]] = relationship(
        back_populates="objeto", cascade="all, delete-orphan"
    )


class ItensDaLista(CentralDeclarativeBase):
    """Modelo ORM para a tabela de itens da lista de compras."""

    __tablename__ = "itens_da_lista"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    listas_de_compras_id: Mapped[int] = mapped_column(
        ForeignKey="listas_de_compras.id"
    )

    nome: Mapped[str] = mapped_column(String(100))
    codigo_de_barras: Mapped[str | None] = mapped_column(String(50))
    preco: Mapped[float | None] = mapped_column(Float)
    categoria: Mapped[str | None] = mapped_column(String(50))
    quantidade: Mapped[int | None] = mapped_column(Integer, default=1)
    local_da_compra: Mapped[str] = mapped_column(String(100))
    data_da_compra: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # relacionamento
    objeto: Mapped["ListasCompras"] = relationship(back_populates="itens")
