from flask_appbuilder.security.sqla.manager import SecurityManager
from app.models.general import ExtendedUser
from app.security.views import ExtendedUserDBModelView, ExtendedUserInfoEditView


class ExtendedSecurityManager(SecurityManager):
    user_model = ExtendedUser
    userdbmodelview = ExtendedUserDBModelView
    userinfoeditview = ExtendedUserInfoEditView
