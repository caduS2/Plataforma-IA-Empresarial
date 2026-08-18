"""cria convites"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "d9e5f7a802c3"
down_revision = "c8f2a9d401b2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "convites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "empresa_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("empresas.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "perfil",
            postgresql.ENUM("ADMIN", "GESTOR", "USUARIO", name="perfil_usuario", create_type=False),
            nullable=False,
        ),
        sa.Column("token", sa.String(length=96), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("expira_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_convites_empresa_id", "convites", ["empresa_id"])
    op.create_index("ix_convites_email", "convites", ["email"])
    op.create_index("ix_convites_token", "convites", ["token"], unique=True)


def downgrade() -> None:
    op.drop_table("convites")
