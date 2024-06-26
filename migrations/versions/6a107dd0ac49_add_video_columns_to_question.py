"""Add video columns to question

Revision ID: 6a107dd0ac49
Revises: 57347e33eb87
Create Date: 2022-05-05 08:59:06.194423

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6a107dd0ac49"
down_revision = "57347e33eb87"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("question", sa.Column("video_url", sa.String(), nullable=True))
    op.add_column("question", sa.Column("video_width", sa.Integer(), nullable=True))
    op.add_column("question", sa.Column("video_height", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("question", "video_height")
    op.drop_column("question", "video_width")
    op.drop_column("question", "video_url")
    # ### end Alembic commands ###
