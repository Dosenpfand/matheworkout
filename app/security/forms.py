from flask_appbuilder.fields import QuerySelectMultipleField, QuerySelectField
from flask_appbuilder.fieldwidgets import Select2ManyWidget, Select2Widget
from flask_appbuilder.forms import DynamicForm

from app import db
from app.models.general import Topic, LearningGroup


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
