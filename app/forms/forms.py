from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_wtf.file import FileField
from wtforms import BooleanField, HiddenField, FloatField, SelectField
from wtforms.validators import NoneOf, DataRequired

from app import db
from app.models.general import Select4Enum, Assignment
from app.utils.general import safe_math_eval
from app.views.widgets import Select2AJAXExtendedWidget


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
    value1 = FlexibleDecimalField(label="Ergebnis 1")
    value2 = FlexibleDecimalField(label="Ergebnis 2")


class Question1DecimalForm(QuestionForm):
    value = FlexibleDecimalField(label="Ergebnis")


class QuestionSelect4Form(QuestionForm):
    selection1 = SelectField(choices=Select4Enum.get_values())
    selection2 = SelectField(choices=Select4Enum.get_values())
    selection3 = SelectField(choices=Select4Enum.get_values())
    selection4 = SelectField(choices=Select4Enum.get_values())


class QuestionSelfAssessedForm(QuestionForm):
    pass


class DeleteStatsForm(DynamicForm):
    user_is_sure = BooleanField(
        label="Bist du sicher?",
        validators=[NoneOf([False], message="Muss ausgewählt sein.")],
    )


class ImportUsersForm(DynamicForm):
    file = FileField(label="CSV-Datei", validators=[DataRequired()])


class AddQuestionToAssignmentForm(DynamicForm):
    model = SQLAInterface(Assignment, db.session)
    assignment_id = AJAXSelectField(
        label="Hausübung",
        datamodel=model,
        validators=[DataRequired()],
        is_related=False,
        widget=Select2AJAXExtendedWidget(
            endpoint="/assignmentmodeladminview/api/readvalues",
            placeholder="Zu Hausübung hinzufügen",
        ),
    )
    question_id = HiddenField()
