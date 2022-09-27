from app import appbuilder
from app.security.views import ExtendedUserDBModelTeacherView, ForgotPasswordFormView, \
    ResetForgotPasswordView
from app.views.forms import QuestionSelfAssessedFormView, Question2of5FormView, Question1of6FormView, \
    Question3to3FormView, Question2DecimalsFormView, Question1DecimalFormView, QuestionSelect4FormView, \
    DeleteStatsFormView
from app.views.general import QuestionRandom, AssignmentModelTeacherView, UtilExtendedView, IdToForm, \
    JoinLearningGroup, DataProtectionView, ImprintView
from app.views.models import Question2of5ModelView, Question1of6ModelView, Question3to3ModelView, \
    Question2DecimalsModelView, Question1DecimalModelView, QuestionSelfAssessedModelView, QuestionSelect4ModelView, \
    QuestionModelView, AssocUserQuestionModelView, AssignmentModelAdminView, AssignmentModelStudentView, \
    QuestionModelIncorrectAnsweredView, QuestionModelCorrectAnsweredView, TopicModelView, LearningGroupModelView, \
    CategoryModelStudentView, CategoryModelAdminView, TopicModelStudentView

appbuilder.add_view(
    LearningGroupModelView,
    'classes',
    label='Klassen',
    icon='fa-book',
    category='Verwaltung',
    category_icon='fa-book')
appbuilder.add_view(
    AssocUserQuestionModelView,
    'answered_questions',
    label='Beantwortete Fragen',
    icon='fa-question',
    category='Verwaltung',
    category_icon='fa-book')
appbuilder.add_view(
    AssignmentModelAdminView,
    'assignments_admin',
    label='Hausübungen',
    icon='fa-tasks',
    category='Verwaltung',
    category_icon='fa-book')
appbuilder.add_view(
    TopicModelView,
    'topics',
    label='Grundkompetenzbereiche',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    CategoryModelAdminView,
    'categories_admin',
    label='Aufgabenkategorien',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_separator('Verwaltung')
appbuilder.add_view(
    Question2of5ModelView,
    'questions_2_of_5',
    label='2 aus 5',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    Question1of6ModelView,
    'questions_1_of_6',
    label='1 aus 6',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    Question3to3ModelView,
    'questions_3_to_3',
    label='Lückentext',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    Question2DecimalsModelView,
    'questions_2_decimals',
    label='Werteingabe zwei Zahlen',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    Question1DecimalModelView,
    'questions_1_decimals',
    label='Werteingabe eine Zahl',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    QuestionSelfAssessedModelView,
    'questions_self_assessed',
    label='Selbstkontrolle',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    QuestionSelect4ModelView,
    'questions_select_4',
    label='Zuordnung',
    icon='fa-align-justify',
    category='Verwaltung',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    AssignmentModelStudentView,
    'assignments_student',
    label='Hausübungen',
    icon='fa-tasks',
    category='questions_category',
    category_label='Aufgabenlisten',
    category_icon='fa-align-justify')
appbuilder.add_view(
    CategoryModelStudentView,
    'questions_categories',
    label='Maturaaufgaben',
    icon='fa-star',
    category='questions_category',
    category_label='Aufgabenlisten',
    category_icon='fa-align-justify')
appbuilder.add_view(
    QuestionModelIncorrectAnsweredView,
    'questions_incorrect',
    label='Falsch beantwortete Aufgaben',
    icon='fa-minus-square',
    category='questions_category',
    category_label='Aufgabenlisten',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    QuestionModelCorrectAnsweredView,
    'questions_correct',
    label='Richtig beantwortete Aufgaben',
    icon='fa-plus-square',
    category='questions_category',
    category_label='Aufgabenlisten',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    TopicModelStudentView,
    'topics',
    label='Grundkompetenzbereiche',
    icon='fa-tags',
    category='questions_category',
    category_label='Aufgabenlisten',
    category_icon='fa-align-justify',
)
appbuilder.add_view(
    QuestionModelView,
    'questions_all',
    label='Alle Aufgaben',
    icon='fa-align-justify',
    category='questions_category',
    category_label='Aufgabenlisten',
    category_icon='fa-align-justify',
)
appbuilder.add_view_no_menu(QuestionRandom())
appbuilder.add_link(
    'random_all',
    label='Zufallsaufgabe',
    href='/questionrandom/',
    icon='fa-question')
appbuilder.add_view_no_menu(Question2of5FormView)
appbuilder.add_view_no_menu(Question1of6FormView)
appbuilder.add_view_no_menu(Question3to3FormView)
appbuilder.add_view_no_menu(Question2DecimalsFormView)
appbuilder.add_view_no_menu(Question1DecimalFormView)
appbuilder.add_view_no_menu(QuestionSelfAssessedFormView)
appbuilder.add_view_no_menu(QuestionSelect4FormView)
appbuilder.add_view_no_menu(IdToForm())
appbuilder.add_view_no_menu(AssignmentModelTeacherView())
appbuilder.add_view_no_menu(UtilExtendedView())
appbuilder.add_view_no_menu(DeleteStatsFormView())
appbuilder.add_view_no_menu(JoinLearningGroup())
appbuilder.add_view_no_menu(ExtendedUserDBModelTeacherView())
appbuilder.add_view_no_menu(ForgotPasswordFormView())
appbuilder.add_view_no_menu(ResetForgotPasswordView())
appbuilder.add_view_no_menu(DataProtectionView())
appbuilder.add_view_no_menu(ImprintView())
