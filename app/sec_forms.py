from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fields import QuerySelectMultipleField, QuerySelectField
from flask_appbuilder.fieldwidgets import Select2ManyWidget, Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired
from .models import Topic
from .sec_models import LearningGroup
from . import db


class ExtendedUserInfoEdit(DynamicForm):
    learning_group = QuerySelectField(
        label='Klasse',
        query_func=lambda: db.session.query(LearningGroup),
        get_pk_func=lambda x: x,
        validators=None,
        widget=Select2Widget()
    )
    active_topics = QuerySelectMultipleField(
        label='Aktive Grundkompetenzbereiche',
        query_func=lambda: db.session.query(Topic),
        get_pk_func=lambda x: x,
        validators=None,
        widget=Select2ManyWidget()
    )
