"""protege tokens de convites"""

import sqlalchemy as sa
from alembic import op

revision = "a3c9e4f106d2"
down_revision = "f2b7c8d104e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("convites", "token", new_column_name="token_hash", existing_type=sa.String(length=96))
    op.alter_column("convites", "token_hash", type_=sa.String(length=64), existing_type=sa.String(length=96))
    op.drop_index("ix_convites_token", table_name="convites")
    op.create_index("ix_convites_token_hash", "convites", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_convites_token_hash", table_name="convites")
    op.alter_column("convites", "token_hash", new_column_name="token", existing_type=sa.String(length=64))
    op.alter_column("convites", "token", type_=sa.String(length=96), existing_type=sa.String(length=64))
    op.create_index("ix_convites_token", "convites", ["token"], unique=True)
