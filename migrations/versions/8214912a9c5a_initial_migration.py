"""Initial migration.

Revision ID: 8214912a9c5a
Revises: 
Create Date: 2022-04-13 09:31:01.899112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8214912a9c5a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("question1_decimal")
    op.drop_table("question1of6")
    op.drop_table("question2_decimals")
    op.drop_table("question_select4")
    op.drop_table("question2of5")
    op.drop_table("question_self_assessed")
    op.drop_table("question3to3")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "question3to3",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("option1a_image", sa.TEXT(), nullable=True),
        sa.Column("option1a_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option1b_image", sa.TEXT(), nullable=True),
        sa.Column("option1b_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option1c_image", sa.TEXT(), nullable=True),
        sa.Column("option1c_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option2a_image", sa.TEXT(), nullable=True),
        sa.Column("option2a_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option2b_image", sa.TEXT(), nullable=True),
        sa.Column("option2b_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option2c_image", sa.TEXT(), nullable=True),
        sa.Column("option2c_is_correct", sa.BOOLEAN(), nullable=True),
        sa.CheckConstraint("option1a_is_correct IN (0, 1)"),
        sa.CheckConstraint("option1b_is_correct IN (0, 1)"),
        sa.CheckConstraint("option1c_is_correct IN (0, 1)"),
        sa.CheckConstraint("option2a_is_correct IN (0, 1)"),
        sa.CheckConstraint("option2b_is_correct IN (0, 1)"),
        sa.CheckConstraint("option2c_is_correct IN (0, 1)"),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "question_self_assessed",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("solution_image", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "question2of5",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("option1_image", sa.TEXT(), nullable=True),
        sa.Column("option1_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option2_image", sa.TEXT(), nullable=True),
        sa.Column("option2_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option3_image", sa.TEXT(), nullable=True),
        sa.Column("option3_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option4_image", sa.TEXT(), nullable=True),
        sa.Column("option4_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option5_image", sa.TEXT(), nullable=True),
        sa.Column("option5_is_correct", sa.BOOLEAN(), nullable=True),
        sa.CheckConstraint("option1_is_correct IN (0, 1)"),
        sa.CheckConstraint("option2_is_correct IN (0, 1)"),
        sa.CheckConstraint("option3_is_correct IN (0, 1)"),
        sa.CheckConstraint("option4_is_correct IN (0, 1)"),
        sa.CheckConstraint("option5_is_correct IN (0, 1)"),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "question_select4",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("selection1_image", sa.TEXT(), nullable=True),
        sa.Column("selection1_solution", sa.VARCHAR(length=1), nullable=True),
        sa.Column("selection2_image", sa.TEXT(), nullable=True),
        sa.Column("selection2_solution", sa.VARCHAR(length=1), nullable=True),
        sa.Column("selection3_image", sa.TEXT(), nullable=True),
        sa.Column("selection3_solution", sa.VARCHAR(length=1), nullable=True),
        sa.Column("selection4_image", sa.TEXT(), nullable=True),
        sa.Column("selection4_solution", sa.VARCHAR(length=1), nullable=True),
        sa.Column("option1_image", sa.TEXT(), nullable=True),
        sa.Column("option2_image", sa.TEXT(), nullable=True),
        sa.Column("option3_image", sa.TEXT(), nullable=True),
        sa.Column("option4_image", sa.TEXT(), nullable=True),
        sa.Column("option5_image", sa.TEXT(), nullable=True),
        sa.Column("option6_image", sa.TEXT(), nullable=True),
        sa.CheckConstraint(
            "selection1_solution IN ('A', 'B', 'C', 'D', 'E', 'F')", name="select4enum"
        ),
        sa.CheckConstraint(
            "selection2_solution IN ('A', 'B', 'C', 'D', 'E', 'F')", name="select4enum"
        ),
        sa.CheckConstraint(
            "selection3_solution IN ('A', 'B', 'C', 'D', 'E', 'F')", name="select4enum"
        ),
        sa.CheckConstraint(
            "selection4_solution IN ('A', 'B', 'C', 'D', 'E', 'F')", name="select4enum"
        ),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "question2_decimals",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("value1_upper_limit", sa.FLOAT(), nullable=True),
        sa.Column("value1_lower_limit", sa.FLOAT(), nullable=True),
        sa.Column("value2_upper_limit", sa.FLOAT(), nullable=True),
        sa.Column("value2_lower_limit", sa.FLOAT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "question1of6",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("option1_image", sa.TEXT(), nullable=True),
        sa.Column("option1_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option2_image", sa.TEXT(), nullable=True),
        sa.Column("option2_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option3_image", sa.TEXT(), nullable=True),
        sa.Column("option3_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option4_image", sa.TEXT(), nullable=True),
        sa.Column("option4_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option5_image", sa.TEXT(), nullable=True),
        sa.Column("option5_is_correct", sa.BOOLEAN(), nullable=True),
        sa.Column("option6_image", sa.TEXT(), nullable=True),
        sa.Column("option6_is_correct", sa.BOOLEAN(), nullable=True),
        sa.CheckConstraint("option1_is_correct IN (0, 1)"),
        sa.CheckConstraint("option2_is_correct IN (0, 1)"),
        sa.CheckConstraint("option3_is_correct IN (0, 1)"),
        sa.CheckConstraint("option4_is_correct IN (0, 1)"),
        sa.CheckConstraint("option5_is_correct IN (0, 1)"),
        sa.CheckConstraint("option6_is_correct IN (0, 1)"),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "question1_decimal",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("external_id", sa.INTEGER(), nullable=True),
        sa.Column("topic_id", sa.INTEGER(), nullable=False),
        sa.Column("description_image", sa.TEXT(), nullable=True),
        sa.Column("value_upper_limit", sa.FLOAT(), nullable=True),
        sa.Column("value_lower_limit", sa.FLOAT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###
