"""empty message

Revision ID: fc01fd2c0c9a
Revises: 6d83a483455a
Create Date: 2022-08-13 14:29:54.127902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fc01fd2c0c9a"
down_revision = "6d83a483455a"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER INDEX association_pkey RENAME TO assoc_assignment_question_pkey")
    op.execute(
        "ALTER TABLE association RENAME CONSTRAINT association_assignment_id_fkey TO assoc_assignment_question_assignment_id_fkey"
    )
    op.execute(
        "ALTER TABLE association RENAME CONSTRAINT association_question_id_fkey TO assoc_assignment_question_question_id_fkey"
    )
    op.rename_table("association", "assoc_assignment_question")


def downgrade():
    op.execute("ALTER INDEX assoc_assignment_question_pkey RENAME TO association_pkey")
    op.execute(
        "ALTER TABLE association RENAME CONSTRAINT assoc_assignment_question_assignment_id_fkey TO association_assignment_id_fkey"
    )
    op.execute(
        "ALTER TABLE association RENAME CONSTRAINT assoc_assignment_question_question_id_fkey TO association_question_id_fkey"
    )
    op.rename_table("assoc_assignment_question", "association")
