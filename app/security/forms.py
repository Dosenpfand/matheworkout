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

from app.models.general import SchoolType


class ForgotPasswordForm(DynamicForm):
    username = StringField()


class ExtendedRegisterUserDBForm(DynamicForm):
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
        "E-Mail-Adresse",
        validators=[DataRequired(), Email()],
        widget=BS3TextFieldWidget(),
    )
    password = PasswordField(
        lazy_gettext("Password"),
        validators=[DataRequired()],
        widget=BS3PasswordFieldWidget(),
    )
    conf_password = PasswordField(
        lazy_gettext("Confirm Password"),
        validators=[
            DataRequired(),
            EqualTo("password", message=lazy_gettext("Passwords must match")),
        ],
        widget=BS3PasswordFieldWidget(),
    )
    # TODO: choices should not be hardcoded
    role = SelectField(
        "Rolle",
        choices=[("Student", "Schüler:in"), ("Teacher", "Lehrer:in")],
        widget=Select2Widget(),
        validators=[DataRequired()],
    )
    school_type = SelectField(
        "Schultyp",
        choices=[(st.name, st.value) for st in SchoolType],
        widget=Select2Widget(),
        validators=[DataRequired()],
    )
    recaptcha = RecaptchaField()


class ExtendedUserInfoEdit(DynamicForm):
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
    school_type = SelectField(
        "Schultyp",
        choices=[(st.name, st.value) for st in SchoolType],
        widget=Select2Widget(),
        validators=[DataRequired()],
    )
