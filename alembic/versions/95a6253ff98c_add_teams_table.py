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
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("nickname", sa.String(), nullable=True),
        sa.Column("stadium", sa.String(), nullable=True),
        sa.Column("competition", sa.String(), nullable=True),
        sa.Column("logo_url_small", sa.String(), nullable=True),
        sa.Column("logo_url_medium", sa.String(), nullable=True),
        sa.Column("logo_url_large", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("twitter_handle", sa.String(), nullable=True),
        sa.Column("national_team", sa.String(), nullable=True),
        sa.Column("year_formed", sa.Integer(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
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
