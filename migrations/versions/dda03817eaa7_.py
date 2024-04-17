"""empty message

Revision ID: dda03817eaa7
Revises: 5663a3aba9dd
Create Date: 2022-08-05 10:38:14.168982

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dda03817eaa7"
down_revision = "5663a3aba9dd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "question", "category_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "question", "category_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###
