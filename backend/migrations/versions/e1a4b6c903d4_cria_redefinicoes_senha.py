"""cria redefinicoes de senha"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "e1a4b6c903d4"
down_revision = "d9e5f7a802c3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "redefinicoes_senha",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("usuario_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token", sa.String(length=96), nullable=False),
        sa.Column("expira_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("usado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_redefinicoes_senha_usuario_id", "redefinicoes_senha", ["usuario_id"])
    op.create_index("ix_redefinicoes_senha_token", "redefinicoes_senha", ["token"], unique=True)


def downgrade() -> None:
    op.drop_table("redefinicoes_senha")
