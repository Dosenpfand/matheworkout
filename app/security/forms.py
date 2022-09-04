from flask_appbuilder.forms import DynamicForm
from wtforms import StringField


class ForgotPasswordForm(DynamicForm):
    username = StringField()