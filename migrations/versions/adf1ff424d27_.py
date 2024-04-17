"""empty message

Revision ID: adf1ff424d27
Revises: 81d2358c376c
Create Date: 2023-04-18 10:50:35.355703

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "adf1ff424d27"
down_revision = "81d2358c376c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "ab_user",
        sa.Column("account_delete_token", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "ab_user", sa.Column("account_delete_expiration", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("ab_user", "account_delete_expiration")
    op.drop_column("ab_user", "account_delete_token")
    # ### end Alembic commands ###
