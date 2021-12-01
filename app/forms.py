from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired


class Question2of5Form(DynamicForm):
    checkbox1 = BooleanField()
    checkbox2 = BooleanField()
    checkbox3 = BooleanField()
    checkbox4 = BooleanField()
    checkbox5 = BooleanField()
