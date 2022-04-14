import app
import sqlite3

cnx = sqlite3.connect('app_single_question_model_20220412.db')
cursor = cnx.cursor()

from app.models import Question1of6, Question1Decimal, Question2Decimals, Question2of5, Question3to3, QuestionSelect4, QuestionSelfAssessed

rows = app.db.session.query(Question1Decimal).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, value1_upper_limit, value1_lower_limit) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'one_decimal', '{row.value_upper_limit}', '{row.value_lower_limit}');")

rows = app.db.session.query(Question2Decimals).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, value1_upper_limit, value1_lower_limit, value2_upper_limit, value2_lower_limit) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'two_decimals', '{row.value1_upper_limit}', '{row.value1_lower_limit}', '{row.value2_upper_limit}', '{row.value2_lower_limit}');")

rows = app.db.session.query(Question1of6).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, option1_image, option1_is_correct, option2_image, option2_is_correct, option3_image, option3_is_correct, option4_image, option4_is_correct, option5_image, option5_is_correct, option6_image, option6_is_correct) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'one_of_six', '{row.option1_image}', '{int(row.option1_is_correct)}', '{row.option2_image}', '{int(row.option2_is_correct)}', '{row.option3_image}', '{int(row.option3_is_correct)}', '{row.option4_image}', '{int(row.option4_is_correct)}', '{row.option5_image}', '{int(row.option5_is_correct)}', '{row.option6_image}', '{int(row.option6_is_correct)}');")

rows = app.db.session.query(Question2of5).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, option1_image, option1_is_correct, option2_image, option2_is_correct, option3_image, option3_is_correct, option4_image, option4_is_correct, option5_image, option5_is_correct) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'two_of_five', '{row.option1_image}', '{int(row.option1_is_correct)}', '{row.option2_image}', '{int(row.option2_is_correct)}', '{row.option3_image}', '{int(row.option3_is_correct)}', '{row.option4_image}', '{int(row.option4_is_correct)}', '{row.option5_image}', '{int(row.option5_is_correct)}');")

rows = app.db.session.query(Question3to3).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, option1a_image, option1a_is_correct, option1b_image, option1b_is_correct, option1c_image, option1c_is_correct, option2a_image, option2a_is_correct, option2b_image, option2b_is_correct, option2c_image, option2c_is_correct) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'three_to_three', '{row.option1a_image}', '{int(row.option1a_is_correct)}', '{row.option1b_image}', '{int(row.option1b_is_correct)}', '{row.option1c_image}', '{int(row.option1c_is_correct)}', '{row.option2a_image}', '{int(row.option2a_is_correct)}', '{row.option2b_image}', '{int(row.option2b_is_correct)}', '{row.option2c_image}', '{int(row.option2c_is_correct)}');")

rows = app.db.session.query(QuestionSelect4).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, selection1_image, selection1_solution, selection3_image, selection2_solution, selection3_image, selection3_solution, selection4_image, selection4_solution, option1_image, option2_image, option3_image, option4_image, option5_image, option6_image) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'select_four', '{row.selection1_image}', '{row.selection1_solution.value}', '{row.selection2_image.value}', '{row.selection2_solution.value}', '{row.selection3_image}', '{row.selection3_solution.value}', '{row.selection4_image}', '{row.selection4_solution.value}', '{row.option1_image}', '{row.option2_image}', '{row.option3_image}', '{row.option4_image}', '{row.option5_image}', '{row.option6_image}');")

rows = app.db.session.query(QuestionSelfAssessed).all()
for row in rows:
    cursor.execute(f"INSERT INTO question (external_id, description_image, topic_id, type, solution_image) VALUES ('{row.external_id}', '{row.description_image}', '{row.topic_id}', 'self_assessed', '{row.solution_image}');")


cnx.commit()
