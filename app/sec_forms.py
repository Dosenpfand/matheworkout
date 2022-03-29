from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_babel import lazy_gettext
from wtforms import IntegerField
from wtforms.validators import DataRequired

class ExtendedUserInfoEdit(DynamicForm):
    tried_questions = IntegerField()
    correct_questions = IntegerField()
