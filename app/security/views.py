import logging
import datetime
import secrets

from flask import g, redirect, url_for, flash, abort, current_app
from flask_appbuilder import action, expose, has_access, PublicFormView
from flask_appbuilder.security.forms import ResetPasswordForm
from flask_appbuilder.security.views import UserDBModelView, UserInfoEditView
from flask_babel import lazy_gettext
from flask_mail import Mail, Message

from app import db
from app.models.general import ExtendedUser
from app.security.forms import ForgotPasswordForm


class ExtendedUserDBModelView(UserDBModelView):
    label_columns = {'username': 'Benutzername', 'learning_groups': 'Klassen', 'tried_questions': 'Gelöste Aufgaben',
                     'correct_questions': 'Richtig gelöste Aufgaben', 'first_name': 'Vorname', 'last_name': 'Nachname',
                     'email': 'E-Mail', 'correct_percentage': 'Anteil richtig'}

    show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'learning_groups', 'tried_questions',
                     'correct_questions', 'correct_percentage']}),
        (lazy_gettext('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
        (lazy_gettext('Audit Info'),
         {'fields': ['last_login', 'fail_login_count', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]

    user_show_fieldsets = [
        (lazy_gettext('User info'),
         {'fields': ['username', 'learning_groups', 'tried_questions', 'correct_questions', 'correct_percentage']}),
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


class ExtendedUserDBModelTeacherView(ExtendedUserDBModelView):
    title = 'Schüler'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    list_columns = [
        'first_name',
        'last_name',
    ]


class ExtendedUserInfoEditView(UserInfoEditView):
    form_title = 'Benutzerinformationen bearbeiten'


class ForgotPasswordFormView(PublicFormView):
    form = ForgotPasswordForm
    form_template = 'forgot_password.html'
    form_title = 'Vergessenes Passwort zurücksetzen'
    email_template = 'password_reset_mail.html'
    email_subject = current_app.config['APP_NAME'] + ' - Passwort zurücksetzen'

    def send_email(self, user):
        mail = Mail(self.appbuilder.get_app)
        msg = Message()
        msg.subject = self.email_subject
        url = url_for('ResetForgotPasswordView.this_form_get', _external=True, user_id=user.id,
                      token=user.password_reset_token)
        msg.html = self.render_template(
            self.email_template,
            url=url,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        msg.recipients = [user.email]
        try:
            mail.send(msg)
        except Exception as e:
            log = logging.getLogger(__name__)
            log.error("Send email exception: {0}".format(str(e)))
            return False
        return True

    @expose("/form", methods=["GET"])
    def this_form_get(self):
        self._init_vars()
        form = self.form.refresh()

        widgets = self._get_edit_widget(form=form)
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
            form=form,
        )

    def form_post(self, form):
        # Get user
        user = db.session.query(ExtendedUser).filter_by(username=form.username.data).first()

        if user:
            # Generate token
            token = secrets.token_urlsafe()
            expiration = datetime.datetime.now() + datetime.timedelta(
                hours=current_app.config['PASSWORD_RESET_TOKEN_EXPIRATION_HOURS'])
            user.password_reset_token = token
            user.password_reset_expiration = expiration
            db.session.commit()

            # Send mail
            self.send_email(user)

        # Flash message
        flash(
            'Falls dieser Benutzer existiert, haben Sie eine E-Mail mit einem Link zum Zurücksetzen des Passworts erhalten',
            'info')
        pass

    @expose("/form", methods=["POST"])
    def this_form_post(self):
        self._init_vars()
        form = self.form.refresh()
        if form.validate_on_submit():
            response = self.form_post(form)
            if not response:
                return redirect(self.get_redirect())
            return response
        else:
            widgets = self._get_edit_widget(form=form)
            return self.render_template(
                self.form_template,
                title=self.form_title,
                widgets=widgets,
                appbuilder=self.appbuilder,
                form=form,
            )


class ResetForgotPasswordView(PublicFormView):
    form = ResetPasswordForm
    form_title = lazy_gettext("Reset Password Form")
    redirect_url = "/"
    message = lazy_gettext("Password Changed")

    def form_get(self, form, user_id, token):
        user = db.session.query(ExtendedUser).filter_by(id=user_id, password_reset_token=token).filter(
            ExtendedUser.password_reset_expiration > datetime.datetime.now()).first()
        return user

    @expose("/form/<int:user_id>/<string:token>", methods=["GET"])
    def this_form_get(self, user_id, token):
        self._init_vars()
        form = self.form.refresh()

        response = self.form_get(form, user_id, token)
        if not response:
            return abort(404)

        widgets = self._get_edit_widget(form=form)
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
            form=form,
        )

    def form_post(self, form, user_id, token):
        user = db.session.query(ExtendedUser).filter_by(id=user_id, password_reset_token=token).filter(
            ExtendedUser.password_reset_expiration > datetime.datetime.now()).first()
        if user:
            self.appbuilder.sm.reset_password(user_id, form.password.data)
            flash(self.message, 'Ihr Passwort wurde geändert, Sie können sich jetzt damit anmelden')
            return redirect(url_for('AuthDBView.login'))
        else:
            return abort(404)

    @expose("/form/<int:user_id>/<string:token>", methods=["POST"])
    def this_form_post(self, user_id, token):
        self._init_vars()
        form = self.form.refresh()
        if form.validate_on_submit():
            response = self.form_post(form, user_id, token)
            if not response:
                return redirect(self.get_redirect())
            return response
        else:
            widgets = self._get_edit_widget(form=form)
            return self.render_template(
                self.form_template,
                title=self.form_title,
                widgets=widgets,
                appbuilder=self.appbuilder,
                form=form,
            )
