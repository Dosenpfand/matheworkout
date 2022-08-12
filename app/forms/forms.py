from flask_appbuilder.forms import DynamicForm
from wtforms import BooleanField, HiddenField, FloatField, SelectField
from wtforms.validators import NoneOf

from app.models.general import Select4Enum
from app.utils.general import safe_math_eval


class FlexibleDecimalField(FloatField):

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist[0] = safe_math_eval(valuelist[0])
        return super(FlexibleDecimalField, self).process_formdata(valuelist)


class QuestionForm(DynamicForm):
    id = HiddenField()


class Question2of5Form(QuestionForm):
    checkbox1 = BooleanField()
    checkbox2 = BooleanField()
    checkbox3 = BooleanField()
    checkbox4 = BooleanField()
    checkbox5 = BooleanField()


class Question1of6Form(QuestionForm):
    checkbox1 = BooleanField()
    checkbox2 = BooleanField()
    checkbox3 = BooleanField()
    checkbox4 = BooleanField()
    checkbox5 = BooleanField()
    checkbox6 = BooleanField()


class Question3to3Form(QuestionForm):
    checkbox1a = BooleanField()
    checkbox1b = BooleanField()
    checkbox1c = BooleanField()
    checkbox2a = BooleanField()
    checkbox2b = BooleanField()
    checkbox2c = BooleanField()


class Question2DecimalsForm(QuestionForm):
    value1 = FlexibleDecimalField(label='Ergebnis 1')
    value2 = FlexibleDecimalField(label='Ergebnis 2')


class Question1DecimalForm(QuestionForm):
    value = FlexibleDecimalField(label='Ergebnis')


class QuestionSelect4Form(QuestionForm):
    selection1 = SelectField(choices=Select4Enum.get_values())
    selection2 = SelectField(choices=Select4Enum.get_values())
    selection3 = SelectField(choices=Select4Enum.get_values())
    selection4 = SelectField(choices=Select4Enum.get_values())


class QuestionSelfAssessedForm(QuestionForm):
    pass


class DeleteStatsForm(DynamicForm):
    user_is_sure = BooleanField(label='Bist du sicher?', validators=[NoneOf([False], message='Muss ausgewählt sein.')])
