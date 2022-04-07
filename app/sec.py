from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.security.views import UserInfoEditView
from .sec_models import ExtendedUser
from .sec_views import ExtendedUserDBModelView
from .sec_forms import ExtendedUserInfoEdit


class ExtendedUserInfoEditView(UserInfoEditView):
    form = ExtendedUserInfoEdit
    form_title = 'Benutzerinformationen bearbeiten'


class ExtendedSecurityManager(SecurityManager):
    user_model = ExtendedUser
    userdbmodelview = ExtendedUserDBModelView
    userinfoeditview = ExtendedUserInfoEditView
