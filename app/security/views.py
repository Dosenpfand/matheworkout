import logging
import datetime

from flask import g, redirect, url_for, flash, current_app, request
from flask_appbuilder import action, expose, has_access, PublicFormView, const
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.forms import ResetPasswordForm, LoginForm_db
from flask_appbuilder.security.registerviews import RegisterUserDBView
from flask_appbuilder.security.views import (
    UserDBModelView,
    UserInfoEditView,
    AuthDBView,
)
from flask_appbuilder.utils.base import get_safe_redirect
from flask_appbuilder.validators import Unique
from flask_babel import lazy_gettext
from flask_login import login_user
from flask import Markup

from app import db
from app.models.general import ExtendedUser
from app.security.forms import ForgotPasswordForm, ExtendedRegisterUserDBForm
from app.utils.general import send_email

log = logging.getLogger(__name__)


class ExtendedUserDBModelView(UserDBModelView):
    label_columns = {
        "username": "Benutzername",
        "learning_groups": "Klassen",
        "tried_questions": "Gelöste Aufgaben",
        "correct_questions": "Richtig gelöste Aufgaben",
        "first_name": "Vorname",
        "last_name": "Nachname",
        "email": "E-Mail",
        "correct_percentage": "Anteil richtig",
    }

    show_fieldsets = [
        (
            lazy_gettext("User info"),
            {
                "fields": [
                    "username",
                    "active",
                    "roles",
                    "login_count",
                    "learning_groups",
                    "tried_questions",
                    "correct_questions",
                    "correct_percentage",
                ]
            },
        ),
        (
            lazy_gettext("Personal Info"),
            {"fields": ["first_name", "last_name", "email"], "expanded": True},
        ),
        (
            lazy_gettext("Audit Info"),
            {
                "fields": [
                    "last_login",
                    "fail_login_count",
                    "created_on",
                    "created_by",
                    "changed_on",
                    "changed_by",
                ],
                "expanded": False,
            },
        ),
    ]

    user_show_fieldsets = [
        (
            lazy_gettext("User info"),
            {
                "fields": [
                    "username",
                    "learning_groups",
                    "tried_questions",
                    "correct_questions",
                    "correct_percentage",
                ]
            },
        ),
        (
            lazy_gettext("Personal Info"),
            {"fields": ["first_name", "last_name", "email"], "expanded": True},
        ),
    ]

    add_columns = [
        "first_name",
        "last_name",
        "username",
        "active",
        "email",
        "roles",
        "learning_groups",
        "password",
        "conf_password",
    ]
    list_columns = [
        "first_name",
        "last_name",
        "username",
        "email",
        "learning_groups",
        "tried_questions",
        "correct_questions",
        "correct_percentage",
        "roles",
    ]
    edit_columns = [
        "first_name",
        "last_name",
        "username",
        "active",
        "email",
        "roles",
        "learning_groups",
    ]

    base_order = ("id", "asc")

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

    # noinspection PyUnusedLocal
    @action(
        "delete_user_stats",
        lazy_gettext("Benutzerstatistik löschen"),
        "",
        "fa-user",
        multiple=False,
    )
    def delete_user_stats(self, item):
        return redirect(url_for("DeleteStatsFormView.this_form_get"))


class ExtendedUserDBModelTeacherView(ExtendedUserDBModelView):
    title = "Schüler"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    list_columns = ["first_name", "last_name", "correct_questions"]

    base_order = ("last_name", "asc")


class ExtendedUserInfoEditView(UserInfoEditView):
    form_title = "Benutzerinformationen bearbeiten"


class ForgotPasswordFormView(PublicFormView):
    form = ForgotPasswordForm
    form_template = "forgot_password.html"
    form_title = "Vergessenes Passwort zurücksetzen"
    email_template = "password_reset_mail.html"
    email_subject = current_app.config["APP_NAME"] + " - Passwort zurücksetzen"

    def send_email(self, user):
        url = url_for(
            "ResetForgotPasswordView.this_form_get",
            _external=True,
            user_id=user.id,
            token=user.password_reset_token,
        )
        html = self.render_template(
            self.email_template,
            url=url,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        return send_email(self.appbuilder.get_app, self.email_subject, html, user.email)

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
        user = (
            db.session.query(ExtendedUser)
            .filter_by(username=form.username.data)
            .first()
        )

        if not user:
            user = (
                db.session.query(ExtendedUser)
                .filter_by(email=form.username.data)
                .first()
            )

        if not user:
            user = (
                db.session.query(ExtendedUser)
                .filter_by(email=form.username.data.lower())
                .first()
            )

        if user:
            self.appbuilder.sm.set_password_reset_token(user)
            self.send_email(user)

        # Flash message
        flash(
            Markup(
                "Falls dieser Benutzer existiert, hast du eine E-Mail mit einem Link zum"
                " Zurücksetzen des Passworts erhalten. <br> <b>Falls du sie in deinem Posteingang nicht findest,"
                " kontrolliere bitte auch den Spam-Ordner.</b>"
            ),
            "info",
        )
        return redirect(self.appbuilder.get_url_for_index)

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

    # noinspection PyMethodOverriding
    def form_get(self, form, user_id, token):
        user = (
            db.session.query(ExtendedUser)
            .filter_by(id=user_id, password_reset_token=token)
            .first()
        )
        if user:
            if user.password_reset_expiration > datetime.datetime.now():
                return user
            else:
                flash(
                    "Der Link zum Passwort setzen ist abgelaufen. Du kannst hier einen neuen beantragen.",
                    category="danger",
                )
        return None

    @expose("/form/<int:user_id>/<string:token>", methods=["GET"])
    def this_form_get(self, user_id, token):
        self._init_vars()
        form = self.form.refresh()

        response = self.form_get(form, user_id, token)
        if not response:
            return redirect(url_for("ForgotPasswordFormView.this_form_get"))

        widgets = self._get_edit_widget(form=form)
        self.update_redirect()
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
            form=form,
        )

    # noinspection PyMethodOverriding
    def form_post(self, form, user_id, token):
        user = (
            db.session.query(ExtendedUser)
            .filter_by(id=user_id, password_reset_token=token)
            .first()
        )
        if user:
            if user.password_reset_expiration > datetime.datetime.now():
                self.appbuilder.sm.reset_password(user_id, form.password.data)
                user.password_reset_token = user.password_reset_expiration = None
                flash(
                    "Dein Passwort wurde geändert, du kannst dich jetzt damit anmelden",
                    category="success",
                )
                return redirect(url_for("ExtendedAuthDBView.login"))
            else:
                flash(
                    "Der Link zum Passwort setzen ist abgelaufen. Du kannst hier einen neuen beantragen.",
                    category="danger",
                )
        return None

    @expose("/form/<int:user_id>/<string:token>", methods=["POST"])
    def this_form_post(self, user_id, token):
        self._init_vars()
        form = self.form.refresh()
        if form.validate_on_submit():
            response = self.form_post(form, user_id, token)
            if not response:
                return redirect(url_for("ForgotPasswordFormView.this_form_get"))
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


class ExtendedRegisterUserDBView(RegisterUserDBView):
    form = ExtendedRegisterUserDBForm
    redirect_url = "/"
    email_subject = current_app.config["APP_NAME"] + " - Kontoaktivierung"

    # noinspection PyMethodOverriding
    def add_registration(self, username, first_name, last_name, email, password, role):
        register_user = self.appbuilder.sm.add_register_user(
            username, first_name, last_name, email, password, role
        )
        if register_user:
            if self.send_email(register_user):
                flash(self.message, "info")
                return register_user
            else:
                flash(self.error_message, "danger")
                self.appbuilder.sm.del_register_user(register_user)
                return None

    @expose("/activation/<string:activation_hash>")
    def activation(self, activation_hash):
        reg = self.appbuilder.sm.find_register_user(activation_hash)
        if not reg:
            log.error(const.LOGMSG_ERR_SEC_NO_REGISTER_HASH.format(activation_hash))
            flash(self.false_error_message, "danger")
            return redirect(self.appbuilder.get_url_for_index)
        # noinspection PyArgumentList
        if not self.appbuilder.sm.add_user(
            username=reg.username,
            email=reg.email,
            first_name=reg.first_name,
            last_name=reg.last_name,
            role=self.appbuilder.sm.find_role(reg.role),
            hashed_password=reg.password,
        ):
            flash(self.error_message, "danger")
            return redirect(self.appbuilder.get_url_for_index)
        else:
            self.appbuilder.sm.del_register_user(reg)
            return self.render_template(
                self.activation_template,
                username=reg.username,
                first_name=reg.first_name,
                last_name=reg.last_name,
                appbuilder=self.appbuilder,
            )

    def form_get(self, form):
        self.add_form_unique_validations(form)

    def form_post(self, form):
        self.add_form_unique_validations(form)
        self.add_registration(
            username=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data,
        )

    def add_form_unique_validations(self, form):
        datamodel_user = self.appbuilder.sm.get_user_datamodel
        datamodel_register_user = self.appbuilder.sm.get_register_user_datamodel
        if len(form.email.validators) == 2:
            form.email.validators.append(Unique(datamodel_user, "email"))
            form.email.validators.append(Unique(datamodel_register_user, "email"))


class ExtendedAuthDBView(AuthDBView):
    login_template = "extended_login_db.html"

    @expose("/login/", methods=["GET", "POST"])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)
        form = LoginForm_db()
        if form.validate_on_submit():
            user = self.appbuilder.sm.auth_user_db(
                form.username.data, form.password.data
            )
            if not user:
                user = self.appbuilder.sm.auth_user_db(
                    form.username.data.lower(), form.password.data
                )
            if not user:
                flash(as_unicode(self.invalid_login_message), "warning")
                return redirect(self.appbuilder.get_url_for_login)
            login_user(user, remember=False)
            next_url = request.args.get("next", "")
            return redirect(get_safe_redirect(next_url))
        return self.render_template(
            self.login_template, title=self.title, form=form, appbuilder=self.appbuilder
        )
