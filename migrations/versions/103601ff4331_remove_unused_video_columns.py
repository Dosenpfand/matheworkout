"""Remove unused video columns

Revision ID: 103601ff4331
Revises: 6a107dd0ac49
Create Date: 2022-05-05 10:42:11.191461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "103601ff4331"
down_revision = "6a107dd0ac49"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("question", "video_width")
    op.drop_column("question", "video_height")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "question",
        sa.Column("video_height", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "question",
        sa.Column("video_width", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
