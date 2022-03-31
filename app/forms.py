from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, SelectMultipleField, BooleanField, HiddenField, DecimalField, SelectField
from wtforms.validators import DataRequired
from .models import Topic, Select4Enum
from . import db


def safe_math_eval(string):
    allowed_chars = "0123456789+-*(). /"
    for char in string:
        if char not in allowed_chars:
            return ''
    return eval(string)


class FlexibleDecimalField(DecimalField):

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = valuelist[0].replace(",", ".")
            valuelist[0] = float(safe_math_eval(valuelist[0]))
        return super(FlexibleDecimalField, self).process_formdata(valuelist)


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


class Question3to3Form(DynamicForm):
    id = HiddenField()
    checkbox1a = BooleanField()
    checkbox1b = BooleanField()
    checkbox1c = BooleanField()
    checkbox2a = BooleanField()
    checkbox2b = BooleanField()
    checkbox2c = BooleanField()


class Question2DecimalsForm(DynamicForm):
    id = HiddenField()
    value1 = FlexibleDecimalField()
    value2 = FlexibleDecimalField()


class Question1DecimalForm(DynamicForm):
    id = HiddenField()
    value = FlexibleDecimalField()


class QuestionSelect4Form(DynamicForm):
    id = HiddenField()
    selection1 = SelectField(choices=[el.value for el in Select4Enum])
    selection2 = SelectField(choices=[el.value for el in Select4Enum])
    selection3 = SelectField(choices=[el.value for el in Select4Enum])
    selection4 = SelectField(choices=[el.value for el in Select4Enum])


class QuestionSelfAssessedForm(DynamicForm):
    id = HiddenField()


class TopicForm(DynamicForm):
    choices = []
    topic = SelectMultipleField(
        choices=choices, validate_choice=False, coerce=int)
