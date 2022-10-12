from flask_appbuilder.fieldwidgets import (
    BS3TextFieldWidget,
    BS3PasswordFieldWidget,
    Select2Widget,
)
from flask_appbuilder.forms import DynamicForm
from flask_babel import lazy_gettext
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class ForgotPasswordForm(DynamicForm):
    username = StringField()


class ExtendedRegisterUserDBForm(DynamicForm):
    username = StringField(
        lazy_gettext("User Name"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
    )
    first_name = StringField(
        lazy_gettext("First Name"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
    )
    last_name = StringField(
        lazy_gettext("Last Name"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
    )
    email = StringField(
        lazy_gettext("Email"),
        validators=[DataRequired(), Email()],
        widget=BS3TextFieldWidget(),
    )
    password = PasswordField(
        lazy_gettext("Password"),
        description=lazy_gettext("Bitte wählen Sie ein sicheres Passwort"),
        validators=[DataRequired()],
        widget=BS3PasswordFieldWidget(),
    )
    conf_password = PasswordField(
        lazy_gettext("Confirm Password"),
        description=lazy_gettext("Please rewrite the password to confirm"),
        validators=[EqualTo("password", message=lazy_gettext("Passwords must match"))],
        widget=BS3PasswordFieldWidget(),
    )
    # TODO: choices should not be hardcoded
    role = SelectField(
        "Rolle",
        choices=[("Student", "Schüler"), ("Teacher", "Lehrer")],
        widget=Select2Widget(),
    )
    recaptcha = RecaptchaField()
