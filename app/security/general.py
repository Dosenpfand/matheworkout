import logging
import uuid

from flask_appbuilder import const
from flask_appbuilder.security.sqla.manager import SecurityManager
from werkzeug.security import generate_password_hash

from app.models.general import ExtendedUser, ExtendedRegisterUser
from app.security.views import ExtendedUserDBModelView, ExtendedUserInfoEditView, ExtendedRegisterUserDBView

log = logging.getLogger(__name__)


class ExtendedSecurityManager(SecurityManager):
    user_model = ExtendedUser
    userdbmodelview = ExtendedUserDBModelView
    userinfoeditview = ExtendedUserInfoEditView
    registeruserdbview = ExtendedRegisterUserDBView
    registeruser_model = ExtendedRegisterUser

    def add_register_user(
        self, username, first_name, last_name, email, password, role
    ):
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
