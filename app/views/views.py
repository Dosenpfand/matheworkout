from app import appbuilder
from app.models.general import VideoCategory
from app.security.views import (
    ExtendedUserDBModelTeacherView,
    ForgotPasswordFormView,
    ResetForgotPasswordView,
)
from app.views.forms import (
    AddQuestionToAssignmentFormView,
    DeleteAccountFormView,
    DeleteStatsFormView,
    ImportUsersFormView,
    Question1DecimalFormView,
    Question1of6FormView,
    Question2DecimalsFormView,
    Question2of5FormView,
    Question3to3FormView,
    QuestionSelect2FormView,
    QuestionSelect4FormView,
    QuestionSelfAssessedFormView,
)
from app.views.general import (
    AchievementsView,
    AssignmentModelEvaluationView,
    CalculatorsView,
    DataProtectionView,
    IdToForm,
    ImprintView,
    JoinLearningGroup,
    ShareAssignment,
    QuestionRandom,
    SupportView,
    UtilExtendedView,
)
from app.views.models import (
    AssignmentModelStudentView,
    AssignmentModelTeacherView,
    AssocUserQuestionModelView,
    CategoryModelAdminView,
    CategoryModelStudentView,
    ClasspadVideoModelView,
    GeogebraVideoModelView,
    LearningGroupModelAdminView,
    LearningGroupModelView,
    NspireVideoModelView,
    Question1DecimalModelView,
    Question1of6ModelView,
    Question2DecimalsModelView,
    Question2of5ModelView,
    Question3to3ModelView,
    QuestionModelCorrectAnsweredView,
    QuestionModelIncorrectAnsweredView,
    QuestionModelView,
    QuestionModelWrappedView,
    QuestionModelTeacherView,
    QuestionSelect2ModelView,
    QuestionSelect4ModelView,
    QuestionSelfAssessedModelView,
    TopicModelStudentView,
    TopicModelView,
    VideoModelView,
)

appbuilder.add_separator(category="Security")
appbuilder.add_view(
    LearningGroupModelAdminView,
    "all_classes",
    label="Alle Klassen",
    icon="fa-book",
    category="Security",
    category_icon="fa-book",
)
# TODO: Activating this results in double injection of its super if its is a related view
# (e.g. in LearningGroupModelView)
# appbuilder.add_view(
#     AssignmentModelAdminView,
#     "all_classes",
#     label="Alle Hausübungen",
#     icon="fa-tasks",
#     category="Security",
#     category_icon="fa-book",
# )
appbuilder.add_view(
    AssocUserQuestionModelView,
    "answered_questions",
    label="Beantwortete Fragen",
    icon="fa-question",
    category="Security",
    category_icon="fa-book",
)
appbuilder.add_view(
    LearningGroupModelView,
    "classes",
    label="Klassen",
    icon="fa-book",
    category="Verwaltung",
    category_icon="fa-book",
)
appbuilder.add_view(
    ImportUsersFormView,
    "import_users",
    label="Schüler:innen importieren",
    icon="fa-file-import",
    category="Verwaltung",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    AssignmentModelTeacherView,
    "assignments_admin",
    label="Hausübungen",
    icon="fa-tasks",
    category="Verwaltung",
    category_icon="fa-book",
)
appbuilder.add_view(
    TopicModelView,
    "topics",
    label="Grundkompetenzbereiche",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    CategoryModelAdminView,
    "categories_admin",
    label="Aufgabenkategorien",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question2of5ModelView,
    "questions_2_of_5",
    label="2 aus 5",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question1of6ModelView,
    "questions_1_of_6",
    label="1 aus 6",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question3to3ModelView,
    "questions_3_to_3",
    label="Lückentext",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question2DecimalsModelView,
    "questions_2_decimals",
    label="Werteingabe zwei Zahlen",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question1DecimalModelView,
    "questions_1_decimals",
    label="Werteingabe eine Zahl",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionSelfAssessedModelView,
    "questions_self_assessed",
    label="Selbstkontrolle",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionSelect4ModelView,
    "questions_select_4",
    label="Zuordnung 4 aus 6",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionSelect2ModelView,
    "questions_select_2",
    label="Zuordnung 2 aus 4",
    icon="fa-align-justify",
    category="AV",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    AssignmentModelStudentView,
    "assignments_student",
    label="Hausübungen",
    icon="fa-tasks",
    category="questions_category",
    category_label="Aufgaben",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    CategoryModelStudentView,
    "questions_categories",
    label="Maturaaufgaben",
    icon="fa-star",
    category="questions_category",
    category_label="Aufgaben",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionModelIncorrectAnsweredView,
    "questions_incorrect",
    label="Falsch beantwortete Aufgaben",
    icon="fa-minus-square",
    category="questions_category",
    category_label="Aufgaben",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionModelCorrectAnsweredView,
    "questions_correct",
    label="Richtig beantwortete Aufgaben",
    icon="fa-plus-square",
    category="questions_category",
    category_label="Aufgaben",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    TopicModelStudentView,
    "topics",
    label="Grundkompetenzbereiche",
    icon="fa-tags",
    category="questions_category",
    category_label="Aufgaben",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionModelView,
    "questions_all",
    label="Alle Aufgaben",
    icon="fa-align-justify",
    category="questions_category",
    category_label="Aufgaben",
    category_icon="fa-align-justify",
)
appbuilder.add_view_no_menu(QuestionModelTeacherView)
appbuilder.add_view_no_menu(QuestionModelWrappedView)
appbuilder.add_view_no_menu(QuestionRandom())
appbuilder.add_link(
    "random_all", label="Zufallsaufgabe", href="/questionrandom/", icon="fa-question"
)
appbuilder.add_view_no_menu(VideoModelView)
appbuilder.add_view(
    GeogebraVideoModelView,
    "geogebra_video",
    label=VideoCategory.geogebra.value,
    icon="fa-mobile-screen",
    category="Videos",
    category_icon="fa-play",
)
appbuilder.add_view(
    ClasspadVideoModelView,
    "classpad_video",
    label=VideoCategory.classpad.value,
    icon="fa-calculator",
    category="Videos",
    category_icon="fa-play",
)
appbuilder.add_view(
    NspireVideoModelView,
    "nspire_video",
    label=VideoCategory.nspire.value,
    icon="fa-calculator",
    category="Videos",
    category_icon="fa-play",
)
appbuilder.add_view_no_menu(Question2of5FormView)
appbuilder.add_view_no_menu(Question1of6FormView)
appbuilder.add_view_no_menu(Question3to3FormView)
appbuilder.add_view_no_menu(Question2DecimalsFormView)
appbuilder.add_view_no_menu(Question1DecimalFormView)
appbuilder.add_view_no_menu(QuestionSelfAssessedFormView)
appbuilder.add_view_no_menu(QuestionSelect4FormView)
appbuilder.add_view_no_menu(QuestionSelect2FormView)
appbuilder.add_view_no_menu(IdToForm)
appbuilder.add_view_no_menu(AssignmentModelEvaluationView)
appbuilder.add_view_no_menu(AddQuestionToAssignmentFormView)
appbuilder.add_view_no_menu(UtilExtendedView)
appbuilder.add_view_no_menu(DeleteStatsFormView)
appbuilder.add_view_no_menu(DeleteAccountFormView)
appbuilder.add_view_no_menu(JoinLearningGroup)
appbuilder.add_view_no_menu(ShareAssignment)
appbuilder.add_view_no_menu(ExtendedUserDBModelTeacherView)
appbuilder.add_view_no_menu(ForgotPasswordFormView)
appbuilder.add_view_no_menu(ResetForgotPasswordView)
appbuilder.add_view_no_menu(DataProtectionView)
appbuilder.add_view_no_menu(ImprintView)
appbuilder.add_view_no_menu(CalculatorsView)
appbuilder.add_view_no_menu(SupportView)
appbuilder.add_view_no_menu(AchievementsView)
