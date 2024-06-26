"""empty message

Revision ID: 867def205fde
Revises: f46d9ee068a8
Create Date: 2023-06-26 15:01:00.994148

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "867def205fde"
down_revision = "f46d9ee068a8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("question", "school_type")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "question",
        sa.Column(
            "school_type",
            postgresql.ENUM("ahs", "bhs", name="schooltype"),
            autoincrement=False,
            nullable=False,
        ),
    )
    # ### end Alembic commands ###
