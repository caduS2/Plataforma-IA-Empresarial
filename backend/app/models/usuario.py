from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

if TYPE_CHECKING:
    from app.models.empresa import Empresa


class PerfilUsuario(str, Enum):
    ADMIN = "admin"
    GESTOR = "gestor"
    USUARIO = "usuario"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    perfil: Mapped[PerfilUsuario] = mapped_column(
        SQLAlchemyEnum(PerfilUsuario, name="perfil_usuario"),
        default=PerfilUsuario.USUARIO,
        nullable=False,
    )
    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    empresa_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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

    empresa: Mapped["Empresa"] = relationship(
        back_populates="usuarios",
    )