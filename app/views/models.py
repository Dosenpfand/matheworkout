from flask import g
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.filters import FilterInFunction, FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.utils.filters import FilterQuestionByAnsweredCorrectness
from app.models.general import Question, LearningGroup, Assignment, Topic, Category
from app.models.relations import AssocUserQuestion
from app.utils.general import get_active_topics, link_formatter_question, state_to_emoji_markup, \
    link_formatter_assignment, \
    link_formatter_category, link_formatter_topic
from app.views.widgets import ExtendedListWidget, ExtendedListNoButtonsWidget


class QuestionModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    base_order = ('external_id', 'asc')
    title = 'Aufgaben'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie', 'state': 'Status'}
    list_columns = ['id', 'topic', 'state']
    formatters_columns = {'id': link_formatter_question, 'state': state_to_emoji_markup}
    page_size = 100
    list_widget = ExtendedListWidget


class AssocUserQuestionModelView(ModelView):
    datamodel = SQLAInterface(AssocUserQuestion)
    list_columns = ['user', 'question', 'created_on', 'is_answer_correct']


class LearningGroupModelView(ModelView):
    datamodel = SQLAInterface(LearningGroup)
    list_columns = ['name']


class AssignmentModelAdminView(ModelView):
    datamodel = SQLAInterface(Assignment)
    list_columns = ['name', 'learning_group', 'additional_links']
    label_columns = {'name': 'Titel',
                     'learning_group': 'Klasse',
                     'starts_on': 'Erhalten am',
                     'is_due_on': 'Fällig am',
                     'additional_links': 'Auswertung'}


class AssignmentModelStudentView(ModelView):
    datamodel = SQLAInterface(Assignment)
    base_filters = [['learning_group_id', FilterEqualFunction, lambda: g.user.learning_group_id]]

    label_columns = {'id': 'Titel',
                     'learning_group': 'Klasse',
                     'starts_on': 'Erhalten am',
                     'is_due_on': 'Fällig am'}
    list_columns = ['id', 'starts_on', 'is_due_on']
    show_columns = ['name', 'starts_on', 'is_due_on']
    title = 'Hausübungen'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]
    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    list_widget = ExtendedListNoButtonsWidget

    formatters_columns = {'id': link_formatter_assignment}


class CategoryModelStudentView(ModelView):
    datamodel = SQLAInterface(Category)

    label_columns = {'id': 'Titel'}
    list_columns = ['id']
    show_columns = ['name']
    title = 'Maturaaufgaben'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]
    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    list_widget = ExtendedListNoButtonsWidget

    formatters_columns = {'id': link_formatter_category}


class TopicModelStudentView(ModelView):
    datamodel = SQLAInterface(Topic)

    label_columns = {'id': 'Titel'}
    list_columns = ['id']
    show_columns = ['name']
    title = 'Grundkompetenzbereiche'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]
    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    list_widget = ExtendedListNoButtonsWidget

    formatters_columns = {'id': link_formatter_topic}


class QuestionModelIncorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics],
                    ['', FilterQuestionByAnsweredCorrectness, False]]
    title = 'Aufgaben (falsch beantwortet)'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class QuestionModelCorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics],
                    ['', FilterQuestionByAnsweredCorrectness, True]]
    title = 'Aufgaben (richtig beantwortet)'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class TopicModelView(ModelView):
    datamodel = SQLAInterface(Topic)


class CategoryModelAdminView(ModelView):
    datamodel = SQLAInterface(Category)
