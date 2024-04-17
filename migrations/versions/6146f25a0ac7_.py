"""empty message

Revision ID: 6146f25a0ac7
Revises: 8263aeba1cc6
Create Date: 2022-08-31 14:41:26.435174

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6146f25a0ac7"
down_revision = "8263aeba1cc6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "learning_group", sa.Column("join_token", sa.String(length=255), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("learning_group", "join_token")
    # ### end Alembic commands ###
