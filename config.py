import os

from flask_appbuilder.const import AUTH_DB

basedir = os.path.abspath(os.path.dirname(__file__))

# NOTE: Set the following secret config parameters in a local .env file:
# FLASK_SECRET_KEY created using secrets.token_urlsafe()
# FLASK_SQLALCHEMY_DATABASE_URI
# FLASK_RECAPTCHA_PUBLIC_KEY
# FLASK_RECAPTCHA_PRIVATE_KEY
# FLASK_MAIL_SERVER
# FLASK_MAIL_PORT
# FLASK_MAIL_USE_TLS
# FLASK_MAIL_USERNAME
# FLASK_MAIL_PASSWORD
# FLASK_MAIL_DEFAULT_SENDER
# SENTRY_DSN (optional, for sentry.io tracing)

CSRF_ENABLED = True
SQLALCHEMY_POOL_RECYCLE = 3
SQLALCHEMY_TRACK_MODIFICATIONS = False

BABEL_DEFAULT_LOCALE = "de"
BABEL_DEFAULT_FOLDER = "translations"
LANGUAGES = {
    "de": {"flag": "at", "name": "German"},
}

FAB_API_MAX_PAGE_SIZE = 100
FAB_PASSWORD_COMPLEXITY_ENABLED = False

STUDENT_ROLE_NAME = "Student"
TEACHER_ROLE_NAME = "Teacher"
ADMIN_ROLE_NAME = "Admin"

FAB_ROLES = {
    STUDENT_ROLE_NAME: [
        ["Question.*", "can_list"],
        ["AssignmentModelStudentView", "can_list"],
        ["AssignmentModelStudentView", "can_show"],
        ["CategoryModelStudentView", "can_list"],
        ["CategoryModelStudentView", "can_show"],
        ["TopicModelStudentView", "can_list"],
        ["TopicModelStudentView", "can_show"],
        ["questions_.*", "menu_access"],
        ["random_.*", "menu_access"],
        ["topics", "menu_access"],
        ["assignments_student", "menu_access"],
        [".*", "can_get"],
        [".*", "can_info"],
        ["ExtendedUserInfoEditView", "can_this_form_get"],
        ["ExtendedUserInfoEditView", "can_this_form_post"],
        ["Question.*", "can_this_form_get"],
        ["Question.*", "can_this_form_post"],
        ["ResetMyPasswordView", "can_this_form_get"],
        ["ResetMyPasswordView", "can_this_form_post"],
        ["DeleteStatsFormView", "can_this_form_get"],
        ["DeleteStatsFormView", "can_this_form_post"],
        [".*", "show_question_details_action"],
        ["ExtendedUserDBModelView", "can_userinfo"],
        ["ExtendedUserDBModelView", "userinfoedit"],
        ["ExtendedUserDBModelView", "resetmypassword"],
        ["ExtendedUserDBModelView", "delete_user_stats"],
        ["QuestionRandom", "can_random_question_redirect"],
        ["IdToForm", "can_id_to_form"],
        ["JoinLearningGroup", "can_join_learning_group"],
    ],
    TEACHER_ROLE_NAME: [
        ["Question.*", "can_list"],
        ["AssignmentModelStudentView", "can_list"],
        ["AssignmentModelStudentView", "can_show"],
        ["CategoryModelStudentView", "can_list"],
        ["CategoryModelStudentView", "can_show"],
        ["TopicModelStudentView", "can_list"],
        ["TopicModelStudentView", "can_show"],
        ["ExtendedUserDBModelTeacherView", "can_delete_relationship"],
        ["questions_.*", "menu_access"],
        ["random_.*", "menu_access"],
        ["topics", "menu_access"],
        [".*", "can_get"],
        [".*", "can_info"],
        [".*", "can_this_form_get"],
        [".*", "can_this_form_post"],
        [".*", "show_question_details_action"],
        ["ExtendedUserDBModelView", "can_userinfo"],
        ["ExtendedUserDBModelView", "userinfoedit"],
        ["ExtendedUserDBModelView", "resetmypassword"],
        ["ExtendedUserDBModelView", "delete_user_stats"],
        ["QuestionRandom", "can_random_question_redirect"],
        ["IdToForm", "can_id_to_form"],
        ["Verwaltung", "menu_access"],
        ["classes", "menu_access"],
        ["assignments_admin", "menu_access"],
        ["import_users", "menu_access"],
        ["LearningGroupModelView", ".*"],
        ["AssignmentModelTeacherView", ".*"],
        ["AssignmentModelEvaluationView", ".*"],
        ["AddQuestionToAssignmentFormView", ".*"],
        ["TopicModelView", "can_list"],
        ["QuestionRandom", "can_random_question_redirect"],
    ],
}

# ------------------------------
# GLOBALS FOR GENERAL APP
# ------------------------------

UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = STUDENT_ROLE_NAME

AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "matheworkout"
APP_THEME = ""
FAB_SECURITY_MANAGER_CLASS = "app.security.general.ExtendedSecurityManager"
FAB_BASE_TEMPLATE = "extended_base.html"
FAB_INDEX_VIEW = "app.views.index.ExtendedIndexView"

SITE_EMAIL = "info@matheworkout.at"

PASSWORD_RESET_TOKEN_EXPIRATION_HOURS = 168
QUESTION_RETRY_MIN_MINUTES = 5
MAX_USER_IMPORTS_PER_DAY = 50
DEBUG_TB_INTERCEPT_REDIRECTS = False
