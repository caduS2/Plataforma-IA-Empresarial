"""cria tabela de documentos

Revision ID: b7e1d3a4c291
Revises: 637f8702b45c
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b7e1d3a4c291"
down_revision: str | Sequence[str] | None = "637f8702b45c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documentos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("empresa_id", sa.UUID(), nullable=False),
        sa.Column("usuario_id", sa.UUID(), nullable=True),
        sa.Column("nome_original", sa.String(length=255), nullable=False),
        sa.Column("caminho_arquivo", sa.String(length=500), nullable=False),
        sa.Column("tipo_mime", sa.String(length=120), nullable=False),
        sa.Column("tamanho_bytes", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_documentos_empresa_id"), "documentos", ["empresa_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_documentos_empresa_id"), table_name="documentos")
    op.drop_table("documentos")
