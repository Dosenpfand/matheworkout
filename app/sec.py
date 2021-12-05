from flask_appbuilder.security.sqla.manager import SecurityManager
from .sec_models import ExtendedUser
from .sec_views import ExtendedUserDBModelView

class ExtendedSecurityManager(SecurityManager):
    user_model = ExtendedUser
    userdbmodelview = ExtendedUserDBModelView
