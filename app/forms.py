from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, SelectMultipleField, BooleanField, HiddenField
from wtforms.validators import DataRequired
from .models import Topic
from . import db


class Question2of5Form(DynamicForm):
    id = HiddenField()
    checkbox1 = BooleanField()
    checkbox2 = BooleanField()
    checkbox3 = BooleanField()
    checkbox4 = BooleanField()
    checkbox5 = BooleanField()

class Question1of6Form(DynamicForm):
    id = HiddenField()
    checkbox1 = BooleanField()
    checkbox2 = BooleanField()
    checkbox3 = BooleanField()
    checkbox4 = BooleanField()
    checkbox5 = BooleanField()
    checkbox6 = BooleanField()

class QuestionSelfAssessedForm(DynamicForm):
    id = HiddenField()

class TopicForm(DynamicForm):
    # result = db.session.query(Topic)
    choices = []
    # for element in result:
    #     choices += [(element.id, element.name)]
    topic = SelectMultipleField(choices=choices, validate_choice=False, coerce=int)
