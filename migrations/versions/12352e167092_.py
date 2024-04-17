"""empty message

Revision ID: 12352e167092
Revises: 867def205fde
Create Date: 2023-07-03 17:04:42.033355

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "12352e167092"
down_revision = "867def205fde"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE questiontype ADD VALUE 'select_two'")


def downgrade():
    # Not supported.
    pass
