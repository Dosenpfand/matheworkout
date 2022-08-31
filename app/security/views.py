from flask import g, redirect, url_for
from flask_appbuilder import action, expose, has_access
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
        learning_groups = [group.id for group in g.user.learning_groups]

    return learning_groups


class ExtendedUserDBModelView(UserDBModelView):
    # TODO: !!!
    # base_filters = [
    #     ['learning_group_id', FilterInFunctionWithNone, get_learning_groups]]

    label_columns = {'username': 'Benutzername', 'learning_groups': 'Klassen', 'tried_questions': 'Gelöste Aufgaben',
                     'correct_questions': 'Richtig gelöste Aufgaben', 'first_name': 'Vorname', 'last_name': 'Nachname',
                     'email': 'E-Mail'}

    show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'learning_groups', 'tried_questions',
                     'correct_questions', 'extra']}),
        (lazy_gettext('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
        (lazy_gettext('Audit Info'),
         {'fields': ['last_login', 'fail_login_count', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]

    user_show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'learning_groups', 'tried_questions', 'correct_questions']}),
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
        'learning_groups',
        'password',
        'conf_password'
    ]
    list_columns = [
        'first_name',
        'last_name',
        'username',
        'email',
        'learning_groups',
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
        'learning_groups',
        'answered_questions'
    ]

    @expose("/userinfo/")
    @has_access
    def userinfo(self):
        actions = dict()
        actions["resetmypassword"] = self.actions.get("resetmypassword")
        actions["delete_user_stats"] = self.actions.get("delete_user_stats")
        actions["userinfoedit"] = self.actions.get("userinfoedit")

        item = self.datamodel.get(g.user.id, self._base_filters)
        widgets = self._get_show_widget(
            g.user.id, item, actions=actions, show_fieldsets=self.user_show_fieldsets
        )
        self.update_redirect()
        return self.render_template(
            self.show_template,
            title=self.user_info_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

    @action(
        "delete_user_stats",
        lazy_gettext("Benutzerstatistik löschen"),
        "",
        "fa-user",
        multiple=False,
    )
    def delete_user_stats(self, item):
        return redirect(url_for('DeleteStatsFormView.this_form_get'))


class ExtendedUserInfoEditView(UserInfoEditView):
    form = ExtendedUserInfoEdit
    form_title = 'Benutzerinformationen bearbeiten'
