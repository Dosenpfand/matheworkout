from app import appbuilder
from app.views.forms import QuestionSelfAssessedFormView, Question2of5FormView, Question1of6FormView, \
    Question3to3FormView, Question2DecimalsFormView, Question1DecimalFormView, QuestionSelect4FormView
from app.views.general import QuestionRandom, AssignmentModelTeacherView, UtilExtendedView, IdToForm
from app.views.models import QuestionModelView, AssocUserQuestionModelView, AssignmentModelAdminView, \
    AssignmentModelStudentView, \
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
    label='Alle Aufgaben',
    href='/questionrandom/',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_separator('random_category')
appbuilder.add_view(
    Question2of5FormView,
    'random_2_of_5',
    label='2 aus 5',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view(
    Question1of6FormView(),
    'random_1_of_6',
    label='1 aus 6',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view(
    Question3to3FormView(),
    'random_3_to_3',
    label='Lückentext',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view(
    Question2DecimalsFormView(),
    'random_2_decimals',
    label='Werteingabe zwei Zahlen',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view(
    Question1DecimalFormView(),
    'random_1_decimal',
    label='Werteingabe eine Zahl',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view(
    QuestionSelfAssessedFormView,
    'random_self_assessed',
    label='Selbstkontrolle',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view(
    QuestionSelect4FormView,
    'random_select_4',
    label='Zuordnung',
    icon='fa-question',
    category='random_category',
    category_label='Zufallsaufgaben',
    category_icon='fa-question')
appbuilder.add_view_no_menu(IdToForm())
appbuilder.add_view_no_menu(AssignmentModelTeacherView())
appbuilder.add_view_no_menu(UtilExtendedView())
