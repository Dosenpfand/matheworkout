from flask_appbuilder.security.views import UserDBModelView
from flask_babel import lazy_gettext


class ExtendedUserDBModelView(UserDBModelView):
    label_columns = {'username': 'Benutzername', 'learning_group': 'Klasse', 'tried_questions': 'Gelöste Aufgaben', 'correct_questions': 'Richtig gelöste Aufgaben', 'first_name': 'Vorname', 'last_name': 'Nachname', 'email': 'E-Mail'}

    show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'learning_group', 'tried_questions', 'correct_questions', 'extra']}),
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
        'active_topics'
    ]
