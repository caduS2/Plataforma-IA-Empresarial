from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    cnpj: Mapped[str | None] = mapped_column(
        String(14),
        unique=True,
        nullable=True,
    )
    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    usuarios: Mapped[list["Usuario"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
