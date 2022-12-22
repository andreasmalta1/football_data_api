"""Add teams table

Revision ID: 95a6253ff98c
Revises: 90034a175358
Create Date: 2022-12-22 18:50:45.073425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "95a6253ff98c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            unique=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    pass


def downgrade() -> None:
    op.drop_table("teams")
    pass
