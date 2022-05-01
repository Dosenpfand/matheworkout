from flask_appbuilder.security.sqla.manager import SecurityManager
from .models import ExtendedUser
from .views import ExtendedUserDBModelView, ExtendedUserInfoEditView


class ExtendedSecurityManager(SecurityManager):
    user_model = ExtendedUser
    userdbmodelview = ExtendedUserDBModelView
    userinfoeditview = ExtendedUserInfoEditView
