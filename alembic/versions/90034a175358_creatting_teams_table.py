"""Creatting teams table

Revision ID: 90034a175358
Revises: 
Create Date: 2022-12-19 17:52:27.512329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "90034a175358"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            unique=True,
        ),
        sa.Column("img", sa.String(), nullable=False, unique=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("mimetype", sa.String(), nullable=False),
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
