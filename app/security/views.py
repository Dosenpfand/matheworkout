import datetime
import logging
import secrets

from flask import Markup, jsonify
from flask import g, redirect, url_for, flash, current_app, request
from flask_appbuilder import action, expose, has_access, PublicFormView
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.forms import ResetPasswordForm, LoginForm_db
from flask_appbuilder.security.registerviews import RegisterUserDBView
from flask_appbuilder.security.views import (
    UserDBModelView,
    UserInfoEditView,
    AuthDBView,
)
from flask_appbuilder.utils.base import is_safe_redirect_url
from flask_appbuilder.validators import Unique
from flask_babel import lazy_gettext
from flask_login import login_user
from flask_mail import Mail, Message

from app import db
from app.models.general import ExtendedUser, LearningGroup
from app.security.forms import (
    ExtendedUserInfoEdit,
    ForgotPasswordForm,
    ExtendedRegisterUserDBForm,
)
from app.utils.general import send_email
from app.views.widgets import ListWithDeleteRelationshipWidget, RegisterFormWidget

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
        "school_type": "Schultyp",
    }

    show_fieldsets = [
        (
            lazy_gettext("User info"),
            {
                "fields": [
                    "username",
                    "active",
                    "roles",
                    "school_type",
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
                    "password_reset_token",
                    "password_reset_expiration",
                    "email_confirmation_token",
                    "account_delete_token",
                    "account_delete_expiration",
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
                    "school_type",
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
        "school_type",
        "learning_groups",
        "password",
        "conf_password",
    ]
    list_columns = [
        "first_name",
        "last_name",
        "email",
        "school_type",
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
        "school_type",
        "learning_groups",
    ]
    search_columns = [
        "first_name",
        "last_name",
        "email",
        "learning_groups",
        "school_type",
        "roles",
        "last_login",
        "created_on",
    ]

    base_order = ("id", "desc")

    @expose("/userinfo/")
    @has_access
    def userinfo(self):
        actions = dict()
        actions["resetmypassword"] = self.actions.get("resetmypassword")
        actions["delete_user_stats"] = self.actions.get("delete_user_stats")
        actions["delete_account"] = self.actions.get("delete_account")
        actions["export_data_action"] = self.actions.get("export_data_action")
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

    @expose("/confirm_account_delete/<int:user_id>/<string:token>")
    @has_access
    def confirm_account_delete(self, user_id: int, token: str):
        if user_id != g.user.id:
            return redirect(url_for("ExtendedIndexView.index"))

        user = (
            db.session.query(ExtendedUser)
            .filter_by(id=user_id, account_delete_token=token)
            .first()
        )

        if user:
            if user.account_delete_expiration > datetime.datetime.now():
                db.session.delete(user)
                db.session.commit()
                flash(
                    "Dein Benutzerkonto inklusive aller Daten wurde erfolgreich gelöscht.",
                    category="success",
                )
            else:
                flash(
                    "Der Link zum Löschen des Benutzerkontos ist abgelaufen. Du kannst hier einen neuen anfordern.",
                    category="danger",
                )
                return redirect(url_for("DeleteAccountFormView.this_form_get"))
        return redirect(url_for("ExtendedIndexView.index"))

    @expose("/export_data")
    @has_access
    def export_data(self):
        return jsonify(g.user.as_export_dict())

    # noinspection PyUnusedLocal
    @action(
        "delete_user_stats",
        "Benutzerstatistik löschen",
        "",
        "fa-user-gear",
        multiple=False,
    )
    def delete_user_stats(self, item):
        return redirect(url_for("DeleteStatsFormView.this_form_get"))

    # noinspection PyUnusedLocal
    @action(
        "delete_account",
        "Benutzerkonto löschen",
        "",
        "fa-user-slash",
        multiple=False,
    )
    def delete_account(self, item):
        return redirect(url_for("DeleteAccountFormView.this_form_get"))

    # noinspection PyUnusedLocal
    @action(
        "export_data_action",
        "Daten exportieren",
        "",
        "fa-download",
        multiple=False,
    )
    def export_data_action(self, item):
        return redirect(url_for(".export_data"))


class ExtendedUserDBModelTeacherView(ExtendedUserDBModelView):
    title = "Schüler:innen"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    list_widget = ListWithDeleteRelationshipWidget

    list_columns = ["first_name", "last_name", "correct_questions"]

    base_order = ("last_name", "asc")

    @expose("/delete_relationship/<int:pk>/<int:fk>", methods=["POST"])
    @has_access
    def delete_relationship(self, pk, fk):
        self.update_redirect()
        learning_group = (
            db.session.query(LearningGroup)
            .filter_by(id=fk, created_by_fk=g.user.id)
            .first()
        )
        user = db.session.query(ExtendedUser).filter_by(id=pk).first()
        if learning_group and user and (user in learning_group.users):
            learning_group.users.remove(user)
            db.session.commit()
            flash("Erfolgreich entfernt", "success")
        else:
            flash("Entfernen fehlgeschlagen", "danger")
        return self.post_delete_redirect()


class ExtendedUserInfoEditView(UserInfoEditView):
    form = ExtendedUserInfoEdit
    form_title = "Benutzerinformationen bearbeiten"

    def form_get(self, form: DynamicForm) -> None:
        user = self.appbuilder.sm.get_user_by_id(g.user.id)

        for field_name, _ in form.data.items():
            if field_name == "csrf_token":
                continue
            elif field_name == "school_type":
                form_field = getattr(form, field_name)
                form_field.data = getattr(user, field_name).name
            else:
                form_field = getattr(form, field_name)
                form_field.data = getattr(user, field_name)


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

        if user and not user.email_confirmation_token:
            self.appbuilder.sm.set_password_reset_token(user)
            self.send_email(user)

        # Flash message
        flash(
            Markup(
                "Falls dieser Benutzer existiert, "
                "hast du eine E-Mail mit einem Link zum Zurücksetzen des Passworts erhalten. <br>"
                "<b>Falls du sie in deinem Posteingang nicht findest, kontrolliere bitte auch den Spam-Ordner.</b>"
            ),
            "info",
        )
        return redirect(url_for("ExtendedIndexView.index"))

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
                    "Der Link zum Passwort setzen ist abgelaufen. Du kannst hier einen neuen anfordern.",
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
    edit_widget = RegisterFormWidget

    @expose("/resend_email")
    @has_access
    def resend_email(self):
        email_is_sent = self.send_email(g.user)

        if email_is_sent:
            flash(
                Markup(
                    "Du solltest die Bestätigungs-Mail erhalten haben.<br>"
                    "<b>Falls du keine E-Mail in deinem Posteingang findest, "
                    "kontrolliere bitte auch den Spam-Ordner.</b>"
                ),
                category="info",
            )
        else:
            flash(
                "Senden der E-Mail fehlgeschlagen. Bitte versuche es später erneut.",
                category="danger",
            )
        return redirect(url_for("ExtendedIndexView.index"))

    @expose("/confirm_email/<int:user_id>/<string:token>", methods=["GET"])
    def confirm_email(self, user_id, token):
        user = (
            db.session.query(ExtendedUser)
            .filter_by(id=user_id, email_confirmation_token=token)
            .first()
        )
        if user:
            user.email_confirmation_token = None
            db.session.commit()
            flash(
                "Du hast deine E-Mail-Adresse erfolgreich bestätigt!",
                category="success",
            )
        else:
            flash(
                "Bestätigung fehlgeschlagen!",
                category="danger",
            )

        if g.user:
            return redirect(url_for("ExtendedIndexView.index"))
        else:
            return redirect(self.appbuilder.get_url_for_login)

    def send_email(self, user: ExtendedUser):
        mail = Mail(self.appbuilder.get_app)
        msg = Message()
        msg.subject = self.email_subject
        url = url_for(
            ".confirm_email",
            _external=True,
            user_id=user.id,
            token=user.email_confirmation_token,
        )
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
            log.error("Send email exception: {0}".format(str(e)))
            return False
        return True

    # noinspection PyMethodOverriding
    def add_registration(
        self, username, first_name, last_name, email, password, role, school_type
    ):
        user = self.appbuilder.sm.add_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=self.appbuilder.sm.find_role(role),
            password=password,
            school_type=school_type,
        )

        if not user:
            flash(self.error_message, "danger")
            return redirect(url_for("ExtendedIndexView.index"))

        user.email_confirmation_token = secrets.token_urlsafe()
        self.appbuilder.session.commit()
        self.send_email(user)
        is_logged_in = login_user(user)

        if is_logged_in:
            flash(
                Markup(
                    "Um den vollen Funktionsumfang zu nutzen, bestätige deine E-Mail-Adresse.<br>"
                    "<b>Falls du keine E-Mail in deinem Posteingang findest, "
                    "kontrolliere bitte auch den Spam-Ordner.</b>"
                ),
                "info",
            )
        else:
            flash("Bitte logge dich ein.", category="info")

        return redirect(current_app.appbuilder.get_url_for_index)

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
            school_type=form.school_type.data,
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
            return redirect(url_for("ExtendedIndexView.index"))
        form = LoginForm_db()
        if form.validate_on_submit():
            user: ExtendedUser = self.appbuilder.sm.auth_user_db(
                form.username.data, form.password.data
            )
            if not user:
                user = self.appbuilder.sm.auth_user_db(
                    form.username.data.lower(), form.password.data
                )
            if not user:
                flash(as_unicode(self.invalid_login_message), "warning")
                return redirect(self.appbuilder.get_url_for_login)

            login_user(user)

            if user.email_confirmation_token:
                url = url_for("ExtendedRegisterUserDBView.resend_email")
                link = Markup(f'<a href="{url}">klicke bitte hier</a>')
                flash(
                    Markup(
                        "Um den vollen Funktionsumfang zu nutzen, bestätige deine E-Mail-Adresse.<br>"
                        "<b>Falls du keine E-Mail in deinem Posteingang findest, "
                        "kontrolliere bitte auch den Spam-Ordner.</b><br>"
                        f"Um die Bestätigungs-Mail erneut zu erhalten {link}."
                    ),
                    "info",
                )

            next_url = request.args.get("next", False)
            if next_url:
                return redirect(get_safe_redirect(next_url))
            else:
                return redirect(current_app.appbuilder.get_url_for_index)

        return self.render_template(
            self.login_template, title=self.title, form=form, appbuilder=self.appbuilder
        )


def get_safe_redirect(url):
    if url and is_safe_redirect_url(url):
        return url
    log.warning(f"Invalid redirect to '{url}' detected, falling back to index")
    return current_app.appbuilder.get_url_for_index
