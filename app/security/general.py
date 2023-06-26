import csv
import datetime
import io
import logging
import secrets
import uuid

from flask import flash, url_for, render_template, g
from flask_appbuilder import const
from flask_appbuilder.security.sqla.manager import SecurityManager
from werkzeug.security import generate_password_hash

from app.models.general import ExtendedUser, LearningGroup, SchoolType
from app.security.views import (
    ExtendedUserDBModelView,
    ExtendedUserInfoEditView,
    ExtendedRegisterUserDBView,
    ExtendedAuthDBView,
)
from app.utils.general import send_email

log = logging.getLogger(__name__)


class ExtendedSecurityManager(SecurityManager):
    user_model = ExtendedUser
    userdbmodelview = ExtendedUserDBModelView
    userinfoeditview = ExtendedUserInfoEditView
    registeruserdbview = ExtendedRegisterUserDBView
    authdbview = ExtendedAuthDBView

    # noinspection PyMethodOverriding
    def add_register_user(self, username, first_name, last_name, email, password, role):
        register_user = self.registeruser_model()
        register_user.username = username
        register_user.email = email
        register_user.first_name = first_name
        register_user.last_name = last_name
        register_user.password = generate_password_hash(password)
        register_user.registration_hash = str(uuid.uuid1())
        register_user.role = role
        try:
            self.get_session.add(register_user)
            self.get_session.commit()
            return register_user
        except Exception as e:
            log.error(const.LOGMSG_ERR_SEC_ADD_REGISTER_USER.format(str(e)))
            self.appbuilder.get_session.rollback()
            return None

    def set_password_reset_token(self, user: ExtendedUser):
        token = secrets.token_urlsafe()
        expiration = datetime.datetime.now() + datetime.timedelta(
            hours=self.appbuilder.app.config["PASSWORD_RESET_TOKEN_EXPIRATION_HOURS"]
        )
        user.password_reset_token = token
        user.password_reset_expiration = expiration
        self.appbuilder.session.commit()

    def set_account_delete_token(self, user: ExtendedUser):
        token = secrets.token_urlsafe()
        expiration = datetime.datetime.now() + datetime.timedelta(
            hours=self.appbuilder.app.config["ACCOUNT_DELETE_TOKEN_EXPIRATION_HOURS"]
        )
        user.account_delete_token = token
        user.account_delete_expiration = expiration
        self.appbuilder.session.commit()

    def import_users(self, csv_data):
        # TODO: for many rows queue is needed! celery?
        # TODO: support UTF-8?
        if g.user.email_confirmation_token:
            flash(
                "Um diese Funktionalität zu nutzen, musst du zuerst deine eigene E-Mail-Adresse bestätigen.",
                category="danger",
            )
            return

        wrapper = io.TextIOWrapper(csv_data, encoding="iso-8859-1")
        csv_reader = csv.DictReader(wrapper, delimiter=";")
        try:
            csv_rows = list(csv_reader)
        except csv.Error as e:
            log.exception(f"Could not read CSV file: {e}")
            flash(
                "Die Datei konnte nicht dekodiert werden. Ist es eine CSV-Datei?",
                category="danger",
            )
        else:
            is_fatal = False
            max_imports_per_day = self.appbuilder.app.config["MAX_USER_IMPORTS_PER_DAY"]

            one_day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)
            count_users_created = (
                self.appbuilder.session.query(ExtendedUser)
                .filter_by(created_by=g.user)
                .filter(ExtendedUser.created_on > one_day_ago)
                .count()
            )

            if count_users_created > max_imports_per_day:
                flash(
                    (
                        f"Import nicht möglich, "
                        f"das tägliches Importlimit von {max_imports_per_day} wurde bereits erreicht."
                    ),
                    category="danger",
                )
                return

            if count_users_created + len(csv_rows) > max_imports_per_day:
                flash(
                    (
                        f"Import nicht möglich, "
                        f"der Import würde das tägliches Importlimit von {max_imports_per_day} überschreiten."
                    ),
                    category="danger",
                )
                return

            try:
                for row in csv_rows:
                    try:
                        first_name = row["Vorname"]
                        last_name = row["Nachname"]
                        email = row["E-Mail-Adresse"]
                        learning_group_name = row["Klasse"]
                    except KeyError as e:
                        flash(
                            "In der Datei konnte die erwartete Spalte {} nicht gefunden werden.".format(
                                e
                            ),
                            category="danger",
                        )
                        is_fatal = True
                        break
                    else:
                        role = self.appbuilder.sm.find_role(
                            self.appbuilder.app.config["AUTH_USER_REGISTRATION_ROLE"]
                        )
                        user = self.add_user(
                            email,
                            first_name,
                            last_name,
                            email,
                            role,
                            hashed_password="NO_PASSWORD_IMPORTED_USER",
                            # Make it impossible to log in, without password reset
                        )

                        if not user:
                            flash(
                                (
                                    f"Konnte den Benutzer '{first_name} {last_name} ({email})' nicht importieren. "
                                    "Möglicherweise existiert bereits ein Benutzer mit dieser E-Mail-Adresse."
                                ),
                                category="danger",
                            )
                        else:
                            learning_group = (
                                self.appbuilder.session.query(LearningGroup)
                                .filter_by(name=learning_group_name, created_by=g.user)
                                .first()
                            )

                            if not learning_group:
                                learning_group = LearningGroup(name=learning_group_name)
                                self.appbuilder.session.add(learning_group)

                            user.learning_groups.append(learning_group)
                            user.school_type = g.user.school_type
                            self.appbuilder.session.commit()

                            self.set_password_reset_token(user)
                            url = url_for(
                                "ResetForgotPasswordView.this_form_get",
                                _external=True,
                                user_id=user.id,
                                token=user.password_reset_token,
                            )
                            subject = f"{self.appbuilder.app.config['APP_NAME']} - Kontoaktivierung"
                            html = render_template(
                                "import_user_password_reset_email.html",
                                url=url,
                                username=user.username,
                                first_name=user.first_name,
                                last_name=user.last_name,
                            )
                            send_email(
                                self.appbuilder.app,
                                subject,
                                html,
                                user.email,
                            )
            except:
                flash(
                    "Die Datei konnte nicht dekodiert werden. Ist es eine CSV-Datei?",
                    category="danger",
                )
                is_fatal = True

            if not is_fatal:
                flash("Import abgeschlossen.", category="info")

    def find_school_type(self, name):
        return SchoolType['name']
