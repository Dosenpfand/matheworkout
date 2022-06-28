from app import appbuilder
from app.views.forms import QuestionSelfAssessedFormView, Question2of5FormView, Question1of6FormView, \
    Question3to3FormView, Question2DecimalsFormView, Question1DecimalFormView, QuestionSelect4FormView
from app.views.general import QuestionRandom, AssignmentModelTeacherView, UtilExtendedView, IdToForm
from app.views.models import Question2of5ModelView, Question1of6ModelView, Question3to3ModelView, \
    Question2DecimalsModelView, Question1DecimalModelView, QuestionSelfAssessedModelView, QuestionSelect4ModelView, \
    QuestionModelView, AssocUserQuestionModelView, AssignmentModelAdminView, AssignmentModelStudentView, \
    QuestionModelIncorrectAnsweredView, QuestionModelCorrectAnsweredView, TopicModelView, LearningGroupModelView, \
    CategoryModelView

appbuilder.add_view(
    LearningGroupModelView,
    "Klassen",
    icon="fa-book",
    category="Verwaltung",
    category_icon="fa-book")
appbuilder.add_view(
    AssocUserQuestionModelView,
    "Beantwortete Fragen",
    icon="fa-question",
    category="Verwaltung",
    category_icon="fa-book")
appbuilder.add_view(
    AssignmentModelAdminView,
    "Hausübungen",
    icon="fa-tasks",
    category="Verwaltung",
    category_icon="fa-book")
appbuilder.add_view(
    TopicModelView,
    "Grundkompetenzbereiche",
    icon="fa-align-justify",
    category="Verwaltung",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    CategoryModelView,
    "Aufgabenkategorien",
    icon="fa-align-justify",
    category="Verwaltung",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    AssignmentModelStudentView,
    "Hausübungen",
    icon="fa-tasks",
    category="Aufgabenlisten",
    category_icon="fa-align-justify")
appbuilder.add_view(
    QuestionModelIncorrectAnsweredView,
    "Falsch beantwortete Aufgaben",
    icon="fa-minus-square",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionModelCorrectAnsweredView,
    "Richtig beantwortete Aufgaben",
    icon="fa-plus-square",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionModelView,
    "Alle Aufgaben",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_separator("Aufgabenlisten")
appbuilder.add_view(
    Question2of5ModelView,
    "2 aus 5",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question1of6ModelView,
    "1 aus 6",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question3to3ModelView,
    "Lückentext",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question2DecimalsModelView,
    "Werteingabe zwei Zahlen",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    Question1DecimalModelView,
    "Werteingabe eine Zahl",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionSelfAssessedModelView,
    "Selbstkontrolle",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionSelect4ModelView,
    "Zuordnung",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view_no_menu(QuestionRandom())
appbuilder.add_link(
    "Alle Aufgaben",
    href="/questionrandom/",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_separator("Zufallsaufgaben")
appbuilder.add_view(
    Question2of5FormView,
    "2 aus 5",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view(
    Question1of6FormView(),
    "1 aus 6",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view(
    Question3to3FormView(),
    "Lückentext",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view(
    Question2DecimalsFormView(),
    "Werteingabe zwei Zahlen",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view(
    Question1DecimalFormView(),
    "Werteingabe eine Zahl",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view(
    QuestionSelfAssessedFormView,
    "Selbstkontrolle",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view(
    QuestionSelect4FormView,
    "Zuordnung",
    icon="fa-question",
    category="Zufallsaufgaben",
    category_icon="fa-question")
appbuilder.add_view_no_menu(IdToForm())
appbuilder.add_view_no_menu(AssignmentModelTeacherView())
appbuilder.add_view_no_menu(UtilExtendedView())
