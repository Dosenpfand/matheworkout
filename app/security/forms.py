from flask_appbuilder.fields import QuerySelectMultipleField
from flask_appbuilder.fieldwidgets import Select2ManyWidget
from flask_appbuilder.forms import DynamicForm

from app import db
from app.models.general import LearningGroup


# TODO: Dead code, delete
class ExtendedUserInfoEdit(DynamicForm):
    learning_groups = QuerySelectMultipleField(
        label='Klassen',
        query_func=lambda: db.session.query(LearningGroup),
        get_pk_func=lambda x: x,
        validators=None,
        widget=Select2ManyWidget()
    )
