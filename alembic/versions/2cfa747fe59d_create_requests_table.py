"""Create requests table

Revision ID: 2cfa747fe59d
Revises: 159726ee3d66
Create Date: 2023-01-03 09:35:17.337626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2cfa747fe59d"
down_revision = "159726ee3d66"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("endpoint", sa.String(), nullable=False),
        sa.Column("method", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("client_host", sa.String(), nullable=False),
        sa.Column("client_port", sa.String(), nullable=False),
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
    op.drop_table("requests")
    pass
