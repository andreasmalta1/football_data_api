"""Add users table

Revision ID: 159726ee3d66
Revises: 95a6253ff98c
Create Date: 2022-12-27 13:52:35.336055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "159726ee3d66"
down_revision = "95a6253ff98c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
