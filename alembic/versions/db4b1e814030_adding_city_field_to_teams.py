"""Adding city field to teams

Revision ID: db4b1e814030
Revises: 2cfa747fe59d
Create Date: 2023-01-09 18:02:56.383941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "db4b1e814030"
down_revision = "2cfa747fe59d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("teams", sa.Column("location", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("teams", "location")
    pass
