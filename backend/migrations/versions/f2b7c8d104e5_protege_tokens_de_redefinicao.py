"""protege tokens de redefinicao de senha"""

from alembic import op
import sqlalchemy as sa


revision = "f2b7c8d104e5"
down_revision = "e1a4b6c903d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("redefinicoes_senha", "token", new_column_name="token_hash", existing_type=sa.String(length=96))
    op.alter_column("redefinicoes_senha", "token_hash", type_=sa.String(length=64), existing_type=sa.String(length=96))
    op.drop_index("ix_redefinicoes_senha_token", table_name="redefinicoes_senha")
    op.create_index("ix_redefinicoes_senha_token_hash", "redefinicoes_senha", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_redefinicoes_senha_token_hash", table_name="redefinicoes_senha")
    op.alter_column("redefinicoes_senha", "token_hash", new_column_name="token", existing_type=sa.String(length=64))
    op.alter_column("redefinicoes_senha", "token", type_=sa.String(length=96), existing_type=sa.String(length=64))
    op.create_index("ix_redefinicoes_senha_token", "redefinicoes_senha", ["token"], unique=True)
