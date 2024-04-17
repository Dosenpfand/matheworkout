"""empty message

Revision ID: 63ba10a926db
Revises: dda03817eaa7
Create Date: 2022-08-08 22:49:46.964807

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "63ba10a926db"
down_revision = "dda03817eaa7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("ab_user", "correct_questions")
    op.drop_column("ab_user", "tried_questions")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "ab_user",
        sa.Column("tried_questions", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "ab_user",
        sa.Column(
            "correct_questions", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
    # ### end Alembic commands ###
