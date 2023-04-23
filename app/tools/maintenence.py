from app.app_factory import db
from app.models.general import Category, Question


def delete_category_and_its_questions(category_name):
    category = db.session.query(Category).filter_by(name=category_name).one()
    questions = db.session.query(Question).filter_by(category_id=category.id).all()
    for question in questions:
        db.session.delete(question)
    db.session.delete(category)
    db.session.commit()
