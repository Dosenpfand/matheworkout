from typing import Optional
from flask import Response, flash, g, get_template_attribute, redirect, session, url_for
from flask_appbuilder import ModelView, action, urltools
from flask_appbuilder.baseviews import expose
from flask_appbuilder.models.sqla.filters import (
    FilterEqual,
    FilterEqualFunction,
    FilterInFunction,
)
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from wtforms import DateField, HiddenField

from app import db
from app.models.general import (
    Assignment,
    AssocUserQuestion,
    Category,
    LearningGroup,
    Question,
    QuestionType,
    Topic,
    Video,
    VideoCategory,
)
from app.security.views import ExtendedUserDBModelTeacherView
from app.utils.filters import (
    FilterQuestionByAnsweredCorrectness,
    FilterQuestionByNotAnsweredCorrectness,
)
from app.utils.general import (
    date_formatter_de,
    link_formatter_assignment,
    link_formatter_assignment_admin,
    link_formatter_category,
    link_formatter_learning_group,
    link_formatter_learning_group_admin,
    link_formatter_question,
    link_formatter_topic,
    link_formatter_topic_abbr,
    link_formatter_video,
    state_to_emoji_markup,
)
from app.utils.video import video_embed_url
from app.views.general import ShowQuestionDetailsMixIn
from app.views.widgets import (
    DatePickerWidgetDe,
    ExtendedListNoButtonsWidget,
    ExtendedListWidget,
    NoSearchWidget,
)


class QuestionBaseModelView(ModelView):
    datamodel = SQLAInterface(Question)
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
    add_form_query_rel_fields = {
        "category": [["school_type", FilterEqualFunction, lambda: g.user.school_type]],
        "topic": [["school_type", FilterEqualFunction, lambda: g.user.school_type]],
    }
    edit_form_query_rel_fields = add_form_query_rel_fields

    def __init__(self, **kwargs):
        self.list_title = self.title
        self.show_title = self.title
        self.add_title = self.title
        self.edit_title = self.title

        self.add_columns = self.columns
        self.edit_columns = self.columns
        self.search_columns = self.columns

        self.add_form_extra_fields = {
            "type": HiddenField(default=self.question_type),
        }
        self.edit_form_extra_fields = self.add_form_extra_fields

        self.base_filters = [["type", FilterEqual, self.question_type]]

        super().__init__(**kwargs)


class Question2of5ModelView(QuestionBaseModelView):
    title = "2 aus 5"
    columns = Question.cols_two_of_five
    question_type = QuestionType.two_of_five.value


class Question1of6ModelView(QuestionBaseModelView):
    title = "1 aus 6"
    columns = Question.cols_one_of_six
    question_type = QuestionType.one_of_six.value


class Question3to3ModelView(QuestionBaseModelView):
    title = "Lückentext"
    columns = Question.cols_three_to_three
    question_type = QuestionType.three_to_three.value


class Question2DecimalsModelView(QuestionBaseModelView):
    title = "Werteingabe zwei Zahlen"
    columns = Question.cols_two_decimals
    question_type = QuestionType.two_decimals.value


class Question1DecimalModelView(QuestionBaseModelView):
    title = "Werteingabe eine Zahl"
    columns = Question.cols_one_decimal
    question_type = QuestionType.one_decimal.value


class QuestionSelfAssessedModelView(QuestionBaseModelView):
    title = "Selbstkontrolle"
    columns = Question.cols_self_assessed
    question_type = QuestionType.self_assessed.value


class QuestionSelect4ModelView(QuestionBaseModelView):
    title = "Zuordnung 4 aus 6"
    columns = Question.cols_select_four
    question_type = QuestionType.select_four.value


class QuestionSelect2ModelView(QuestionBaseModelView):
    title = "Zuordnung 2 aus 4"
    columns = Question.cols_select_two
    question_type = QuestionType.select_two.value


# TODO: Inherit from QuestionBaseModelView?
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

    base_order = ("id", "desc")
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

    def _show(self, pk: int):
        pages = urltools.get_page_args()
        page_sizes = urltools.get_page_size_args()
        orders = urltools.get_order_args()

        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            unfiltered_item: Optional[Assignment] = self.datamodel.get(pk)
            if not unfiltered_item:
                flash("Hausübung konnte nicht gefunden werden.", "danger")
                return redirect(self.appbuilder.get_url_for_index)
            elif unfiltered_item.created_by.id == g.user.id:
                item = unfiltered_item
                flash("Dies ist eine Vorschau für Lehrer:innen.", "info")
            else:
                flash(
                    "Du bist nicht berechtigt diese Hausübung zu sehen. Bist du der Klasse bereits beigetreten?",
                    "danger",
                )
                return redirect(self.appbuilder.get_url_for_index)
        widgets = self._get_show_widget(pk, item)
        self.update_redirect()
        return self._get_related_views_widgets(
            item, orders=orders, pages=pages, page_sizes=page_sizes, widgets=widgets
        )

    @expose("/show/<pk>", methods=["GET"])
    @has_access
    def show(self, pk):
        pk = self._deserialize_pk_if_composite(pk)
        widgets = self._show(pk)
        if isinstance(widgets, Response):
            return widgets
        return self.render_template(
            self.show_template,
            pk=pk,
            title=self.show_title,
            widgets=widgets,
            related_views=self._related_views,
        )


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


yt_embed = get_template_attribute("youtube_embed.html", "youtube_embed")


class VideoModelView(ModelView):
    datamodel = SQLAInterface(Video)
    title = "Video"
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {
        "id": "Name",
        "name": "Name",
        "category": "Kategorie",
        "video_url": "Video",
    }
    list_columns = ["id"]
    add_columns = ["name", "video_url"]
    show_columns = ["name", "video_url"]
    search_exclude_columns = ["video_url", "category"]
    formatters_columns = {
        "id": link_formatter_video,
        "video_url": lambda url: yt_embed(
            url=video_embed_url(url), width="100%", height="512"
        ),
    }
    list_widget = ExtendedListNoButtonsWidget


class GeogebraVideoModelView(VideoModelView):
    title = VideoCategory.geogebra.value
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    base_filters = [["category", FilterEqual, VideoCategory.geogebra.name]]

    def pre_add(self, item):
        item.category = VideoCategory.geogebra


class ClasspadVideoModelView(VideoModelView):
    title = VideoCategory.classpad.value
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    base_filters = [["category", FilterEqual, VideoCategory.classpad.name]]

    def pre_add(self, item):
        item.category = VideoCategory.classpad


class NspireVideoModelView(VideoModelView):
    title = VideoCategory.nspire.value
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    base_filters = [["category", FilterEqual, VideoCategory.nspire.name]]

    def pre_add(self, item):
        item.category = VideoCategory.nspire


class TopicModelView(ModelView):
    datamodel = SQLAInterface(Topic)

    list_columns = ["name", "school_type"]


class CategoryModelAdminView(ModelView):
    datamodel = SQLAInterface(Category)

    list_columns = ["name", "school_type"]
