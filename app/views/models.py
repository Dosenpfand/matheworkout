from flask import g, redirect, url_for, flash, session
from flask_appbuilder import ModelView, action
from flask_appbuilder.models.sqla.filters import (
    FilterEqual,
    FilterEqualFunction,
    FilterInFunction,
)
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import HiddenField, DateField

from app import db
from app.models.general import (
    Question,
    QuestionType,
    LearningGroup,
    Assignment,
    Topic,
    Category,
    AssocUserQuestion,
)
from app.security.views import ExtendedUserDBModelTeacherView
from app.utils.filters import (
    FilterQuestionByAnsweredCorrectness,
    FilterQuestionByNotAnsweredCorrectness,
)
from app.utils.general import (
    link_formatter_question,
    state_to_emoji_markup,
    link_formatter_assignment,
    link_formatter_category,
    link_formatter_topic,
    link_formatter_topic_abbr,
    link_formatter_learning_group,
    link_formatter_assignment_admin,
    date_formatter_de,
    link_formatter_learning_group_admin,
)
from app.views.general import ShowQuestionDetailsMixIn
from app.views.widgets import (
    ExtendedListWidget,
    ExtendedListNoButtonsWidget,
    DatePickerWidgetDe,
    NoSearchWidget,
)


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.two_of_five.value]]
    title = "2 aus 5"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_two_of_five
    search_columns = Question.cols_two_of_five
    add_form_extra_fields = {
        "type": HiddenField(default=QuestionType.two_of_five.value)
    }
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "title"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class Question1of6ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.one_of_six.value]]
    title = "1 aus 6"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_one_of_six
    search_columns = Question.cols_one_of_six
    add_form_extra_fields = {"type": HiddenField(default=QuestionType.one_of_six.value)}
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "title"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class Question3to3ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.three_to_three.value]]
    title = "Lückentext"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_three_to_three
    search_columns = Question.cols_three_to_three
    add_form_extra_fields = {
        "type": HiddenField(default=QuestionType.three_to_three.value)
    }
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "title"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class Question2DecimalsModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.two_decimals.value]]
    title = "Werteingabe zwei Zahlen"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_two_decimals
    search_columns = Question.cols_two_decimals
    add_form_extra_fields = {
        "type": HiddenField(default=QuestionType.two_decimals.value)
    }
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "title"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class Question1DecimalModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.one_decimal.value]]
    title = "Werteingabe eine Zahl"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_one_decimal
    search_columns = Question.cols_one_decimal
    add_form_extra_fields = {
        "type": HiddenField(default=QuestionType.one_decimal.value)
    }
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "title"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class QuestionSelfAssessedModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.self_assessed.value]]
    title = "Selbstkontrolle"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_self_assessed
    search_columns = Question.cols_self_assessed
    add_form_extra_fields = {
        "type": HiddenField(default=QuestionType.self_assessed.value)
    }
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "solution_image_img"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class QuestionSelect4ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.select_four.value]]
    title = "Zuordnung 4 aus 6"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_select_four
    search_columns = Question.cols_select_four
    add_form_extra_fields = {
        "type": HiddenField(default=QuestionType.select_four.value)
    }
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "solution_image_img"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class QuestionSelect2ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["type", FilterEqual, QuestionType.select_two.value]]
    title = "Zuordnung 2 aus 4"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_select_two
    search_columns = Question.cols_select_two
    add_form_extra_fields = {"type": HiddenField(default=QuestionType.select_two.value)}
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic"]
    show_columns = ["description_image_img", "solution_image_img"]
    formatters_columns = {"id": link_formatter_question}
    page_size = 100


class QuestionModelView(ModelView):
    def get_topic_ids_for_school_type():
        topics = db.session.query(Topic).filter_by(school_type=g.user.school_type).all()
        return [topic.id for topic in topics]

    datamodel = SQLAInterface(Question)
    base_filters = [["topic_id", FilterInFunction, get_topic_ids_for_school_type]]

    base_order = ("external_id", "asc")
    search_widget = NoSearchWidget
    list_template = "list_no_search.html"
    title = "Aufgaben"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
        "state": "Status",
    }
    list_columns = ["id", "topic", "category", "state"]
    formatters_columns = {
        "id": link_formatter_question,
        "state": state_to_emoji_markup,
        "topic": link_formatter_topic_abbr,
    }
    common_col_count = len(Question.cols_common)
    edit_columns = (
        Question.cols_common
        + Question.cols_self_assessed[common_col_count:]
        + Question.cols_two_decimals[common_col_count:]
        + Question.cols_one_of_six[common_col_count:]
        + Question.cols_select_four[common_col_count:]
        + Question.cols_select_two[common_col_count:]
        + Question.cols_three_to_three[common_col_count:]
    )

    page_size = 50
    list_widget = ExtendedListWidget

    @action(
        "add_questions_to_assignment",
        "Auswahl zu Hausübung hinzufügen",
        confirmation=None,
        icon="fa-tasks",
        multiple=True,
        single=False,
    )
    def add_questions_to_assignment(self, items):
        question_ids = [question.id for question in items]
        session["question_ids_to_add_to_assignment"] = question_ids
        return redirect(url_for("AddQuestionToAssignmentFormView.this_form_get"))


class AssocUserQuestionModelView(ModelView):
    datamodel = SQLAInterface(AssocUserQuestion)
    list_columns = ["user", "question", "created_on", "is_answer_correct"]
    base_order = ("created_on", "des")


class AssignmentModelTeacherView(ModelView, ShowQuestionDetailsMixIn):
    datamodel = SQLAInterface(Assignment)
    base_filters = [["created_by", FilterEqualFunction, lambda: g.user]]

    list_columns = ["id", "learning_group", "additional_links"]

    formatters_columns = {"id": link_formatter_assignment_admin}

    add_columns = [
        "name",
        "learning_group",
        "assigned_questions",
        "starts_on",
        "is_due_on",
    ]
    edit_columns = [
        "name",
        "learning_group",
        "assigned_questions",
        "starts_on",
        "is_due_on",
    ]
    show_columns = [
        "name",
        "learning_group",
        "starts_on_de",
        "is_due_on_de",
        "student_link",
    ]

    extra_fields = {
        "starts_on": DateField(
            "Erhalten am",
            format="%d.%m.%Y",
            widget=DatePickerWidgetDe(),
        ),
        "is_due_on": DateField(
            "Fällig am",
            format="%d.%m.%Y",
            widget=DatePickerWidgetDe(),
        ),
    }

    add_form_extra_fields = extra_fields
    edit_form_extra_fields = extra_fields

    label_columns = {
        "id": "Titel",
        "name": "Titel",
        "learning_group": "Klasse",
        "starts_on": "Erhalten am",
        "is_due_on": "Fällig am",
        "starts_on_de": "Erhalten am",
        "is_due_on_de": "Fällig am",
        "assigned_questions": "Fragen",
        "additional_links": "Auswertung",
        "student_link": "Link für Schüler",
    }

    title = "Hausübungen"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]

    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"

    add_form_query_rel_fields = {
        "learning_group": [["created_by", FilterEqualFunction, lambda: g.user]]
    }
    edit_form_query_rel_fields = {
        "learning_group": [["created_by", FilterEqualFunction, lambda: g.user]]
    }

    questions_col_name = "assigned_questions"

    @action(
        "duplicate_assignment",
        "Hausübung duplizieren",
        confirmation=None,
        icon="fa-paste",
        multiple=False,
    )
    def duplicate_assignment(self, item):
        duplicated = item.duplicate()
        db.session.add(duplicated)
        db.session.commit()

        url = url_for(f"{self.__class__.__name__}.list")
        flash("Hausübung dupliziert", "info")
        return redirect(url)


class AssignmentModelAdminView(AssignmentModelTeacherView):
    base_filters = None


class LearningGroupModelView(ModelView):
    datamodel = SQLAInterface(LearningGroup)
    base_filters = [["created_by", FilterEqualFunction, lambda: g.user]]

    label_columns = {
        "id": "Name",
        "name": "Name",
        "users": "Schüler",
        "join_url": "Link zum Beitreten",
    }

    list_columns = ["id"]
    add_columns = ["name"]
    edit_columns = ["name"]
    show_columns = ["name", "join_url"]

    formatters_columns = {"id": link_formatter_learning_group}

    title = "Klassen"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [AssignmentModelTeacherView, ExtendedUserDBModelTeacherView]

    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"


class LearningGroupModelAdminView(LearningGroupModelView):
    base_filters = None
    show_columns = LearningGroupModelView.show_columns + ["created_by", "user_count"]
    list_columns = LearningGroupModelView.list_columns + ["created_by", "user_count"]
    formatters_columns = {"id": link_formatter_learning_group_admin}


class AssignmentModelStudentView(ModelView, ShowQuestionDetailsMixIn):
    datamodel = SQLAInterface(Assignment)
    base_filters = [
        [
            "learning_group_id",
            FilterInFunction,
            lambda: [group.id for group in g.user.learning_groups],
        ]
    ]

    label_columns = {
        "id": "Titel",
        "learning_group": "Klasse",
        "starts_on_de": "Erhalten am",
        "is_due_on_de": "Fällig am",
        "starts_on": "Erhalten am",
        "is_due_on": "Fällig am",
    }
    list_columns = ["id", "starts_on", "is_due_on"]
    show_columns = ["name", "starts_on_de", "is_due_on_de"]

    title = "Hausübungen"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]

    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    list_widget = ExtendedListNoButtonsWidget

    formatters_columns = {
        "id": link_formatter_assignment,
        "is_due_on": date_formatter_de,
        "starts_on": date_formatter_de,
    }

    questions_col_name = "assigned_questions"


class CategoryModelStudentView(ModelView, ShowQuestionDetailsMixIn):
    datamodel = SQLAInterface(Category)
    base_order = ("name", "desc")
    base_filters = [["school_type", FilterEqualFunction, lambda: g.user.school_type]]

    label_columns = {"id": "Titel"}
    list_columns = ["id"]
    show_columns = ["name"]
    title = "Maturaaufgaben"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]
    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    list_widget = ExtendedListNoButtonsWidget

    formatters_columns = {"id": link_formatter_category}


class TopicModelStudentView(ModelView, ShowQuestionDetailsMixIn):
    datamodel = SQLAInterface(Topic)
    base_filters = [["school_type", FilterEqualFunction, lambda: g.user.school_type]]

    label_columns = {"id": "Titel", "count": "Anzahl"}
    list_columns = ["count", "id"]
    show_columns = ["name"]
    title = "Grundkompetenzbereiche"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]
    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    list_widget = ExtendedListNoButtonsWidget

    formatters_columns = {"id": link_formatter_topic}
    base_order = ("id", "asc")
    page_size = 100

    @action(
        "random_question",
        "Zufallsaufgabe",
        confirmation=None,
        icon="fa-question",
        multiple=False,
    )
    def random_question(self, item):
        url = url_for("QuestionRandom.random_question_redirect", topic_id=item.id)
        return redirect(url)


class QuestionModelIncorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [
        ["", FilterQuestionByAnsweredCorrectness, False],
        ["", FilterQuestionByNotAnsweredCorrectness, True],
    ]
    search_widget = NoSearchWidget
    list_template = "list_no_search.html"

    title = "Falsch beantwortete Aufgaben"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic", "category"]
    formatters_columns = {
        "id": link_formatter_question,
        "topic": link_formatter_topic_abbr,
    }
    page_size = 100


class QuestionModelCorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [["", FilterQuestionByAnsweredCorrectness, True]]
    search_widget = NoSearchWidget
    list_template = "list_no_search.html"

    title = "Richtig beantwortete Aufgaben"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {
        "description_image": "Beschreibung",
        "id": "Frage Nr.",
        "topic": "Grundkompetenzbereich",
        "category": "Kategorie",
    }
    list_columns = ["id", "topic", "category"]
    formatters_columns = {
        "id": link_formatter_question,
        "topic": link_formatter_topic_abbr,
    }
    page_size = 100


class TopicModelView(ModelView):
    datamodel = SQLAInterface(Topic)

    list_columns = ["name", "school_type"]


class CategoryModelAdminView(ModelView):
    datamodel = SQLAInterface(Category)

    list_columns = ["name", "school_type"]
