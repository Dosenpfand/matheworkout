from flask import g
from flask_appbuilder.security.views import UserDBModelView, UserInfoEditView
from flask_babel import lazy_gettext

from app.security.forms import ExtendedUserInfoEdit
from config import AUTH_ROLE_ADMIN
from app import db
from app.utils.filters import FilterInFunctionWithNone
from app.models.general import LearningGroup


def get_learning_groups():
    if AUTH_ROLE_ADMIN in [role.name for role in g.user.roles]:
        result = db.session.query(LearningGroup).all()
        learning_groups = [group.id for group in result] + [None]
    else:
        learning_groups = [g.user.learning_group_id]

    return learning_groups


class ExtendedUserDBModelView(UserDBModelView):
    base_filters = [
        ['learning_group_id', FilterInFunctionWithNone, get_learning_groups]]

    label_columns = {'username': 'Benutzername', 'learning_group': 'Klasse', 'tried_questions': 'Gelöste Aufgaben',
                     'correct_questions': 'Richtig gelöste Aufgaben', 'first_name': 'Vorname', 'last_name': 'Nachname',
                     'email': 'E-Mail'}

    show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'learning_group', 'tried_questions',
                     'correct_questions', 'extra']}),
        (lazy_gettext('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
        (lazy_gettext('Audit Info'),
         {'fields': ['last_login', 'fail_login_count', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]

    user_show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'learning_group', 'tried_questions', 'correct_questions']}),
        (lazy_gettext('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
    ]

    add_columns = [
        'first_name',
        'last_name',
        'username',
        'active',
        'email',
        'roles',
        'learning_group',
        'tried_questions',
        'correct_questions',
        'password',
        'conf_password'
    ]
    list_columns = [
        'first_name',
        'last_name',
        'username',
        'email',
        'learning_group',
        'tried_questions',
        'correct_questions',
        'correct_percentage',
        'roles'
    ]
    edit_columns = [
        'first_name',
        'last_name',
        'username',
        'active',
        'email',
        'roles',
        'learning_group',
        'tried_questions',
        'correct_questions',
        'active_topics',
        'answered_questions'
    ]


class ExtendedUserInfoEditView(UserInfoEditView):
    form = ExtendedUserInfoEdit
    form_title = 'Benutzerinformationen bearbeiten'
