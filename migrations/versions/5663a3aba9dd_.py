"""empty message

Revision ID: 5663a3aba9dd
Revises: 23c87f39cb4a
Create Date: 2022-08-05 09:18:24.939186

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5663a3aba9dd"
down_revision = "23c87f39cb4a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "topic",
        "name",
        existing_type=sa.VARCHAR(length=150),
        type_=sa.String(length=500),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "topic",
        "name",
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=150),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
