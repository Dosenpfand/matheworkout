from flask import g, redirect, url_for, abort
from flask_appbuilder import ModelView, action, expose, has_access
from flask_appbuilder.models.sqla.filters import FilterEqual, FilterEqualFunction, FilterNotEqual, FilterInFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import HiddenField

from app.security.views import ExtendedUserDBModelTeacherView
from app.utils.filters import FilterQuestionByAnsweredCorrectness
from app.models.general import Question, QuestionType, LearningGroup, Assignment, Topic, Category, AssocUserQuestion
from app.utils.general import link_formatter_question, state_to_emoji_markup, \
    link_formatter_assignment, \
    link_formatter_category, link_formatter_topic, link_formatter_topic_abbr
from app.views.widgets import ExtendedListWidget, ExtendedListNoButtonsWidget, ExtendedShowWidget


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.two_of_five.value]]
    title = '2 aus 5'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_two_of_five
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.two_of_five.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class Question1of6ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.one_of_six.value]]
    title = '1 aus 6'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_one_of_six
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.one_of_six.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class Question3to3ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.three_to_three.value]]
    title = 'Lückentext'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_three_to_three
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.three_to_three.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class Question2DecimalsModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.two_decimals.value]]
    title = 'Werteingabe zwei Zahlen'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_two_decimals
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.two_decimals.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class Question1DecimalModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.one_decimal.value]]
    title = 'Werteingabe eine Zahl'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_one_decimal
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.one_decimal.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class QuestionSelfAssessedModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.self_assessed.value]]
    title = 'Selbstkontrolle'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_self_assessed
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.self_assessed.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class QuestionSelect4ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['type', FilterEqual, QuestionType.select_four.value]]
    title = 'Zuordnung'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    add_columns = Question.cols_select_four
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.select_four.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'id': link_formatter_question}
    page_size = 100


class QuestionModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = []
    base_order = ('external_id', 'asc')
    title = 'Aufgaben'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie', 'state': 'Status'}
    list_columns = ['id', 'topic', 'category', 'state']
    formatters_columns = {'id': link_formatter_question, 'state': state_to_emoji_markup,
                          'topic': link_formatter_topic_abbr}

    page_size = 100
    list_widget = ExtendedListWidget


class AssocUserQuestionModelView(ModelView):
    datamodel = SQLAInterface(AssocUserQuestion)
    list_columns = ['user', 'question', 'created_on', 'is_answer_correct']


class AssignmentModelAdminView(ModelView):
    datamodel = SQLAInterface(Assignment)
    base_filters = [['created_by', FilterEqualFunction, lambda: g.user]]

    list_columns = ['name', 'learning_group', 'additional_links']
    add_columns = ['name', 'learning_group', 'assigned_questions', 'starts_on', 'is_due_on']
    edit_columns = ['name', 'learning_group', 'assigned_questions', 'starts_on', 'is_due_on']
    show_columns = ['name', 'learning_group', 'starts_on', 'is_due_on', 'student_link']

    label_columns = {'name': 'Titel',
                     'learning_group': 'Klasse',
                     'starts_on': 'Erhalten am',
                     'is_due_on': 'Fällig am',
                     'assigned_questions': 'Fragen',
                     'additional_links': 'Auswertung',
                     'student_link': 'Link für Schüler'}

    title = 'Hausübungen'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [QuestionModelView]

    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"

    add_form_query_rel_fields = {'learning_group': [['created_by', FilterEqualFunction, lambda: g.user]]}
    edit_form_query_rel_fields = {'learning_group': [['created_by', FilterEqualFunction, lambda: g.user]]}


class LearningGroupModelView(ModelView):
    datamodel = SQLAInterface(LearningGroup)
    base_filters = [['created_by', FilterEqualFunction, lambda: g.user]]

    label_columns = {'name': 'Name', 'users': 'Schüler', 'join_url': 'Link zum Beitreten'}

    list_columns = ['name']
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name', 'join_url']

    title = 'Klassen'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title

    related_views = [AssignmentModelAdminView, ExtendedUserDBModelTeacherView]

    show_template = "show_cascade_expanded.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"
    # TODO: not needed?
    # list_widget = ExtendedListNoButtonsWidget


class AssignmentModelStudentView(ModelView):
    datamodel = SQLAInterface(Assignment)
    base_filters = [['learning_group_id', FilterInFunction, lambda: [group.id for group in g.user.learning_groups]]]

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
    base_filters = [['name', FilterNotEqual, 'Aufgabenpool']]

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
    edit_widget = ExtendedShowWidget

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
    base_order = ('id', 'asc')
    page_size = 100

    @action('random_question', 'Zufallsaufgabe', confirmation=None, icon='fa-question', multiple=False)
    def random_question(self, item):
        url = url_for('QuestionRandom.random_question_redirect', topic_id=item.id)
        return redirect(url)

    @expose("/show_detail/<pk>", methods=["GET"])
    @has_access
    def show_detail(self, pk):
        pk = self._deserialize_pk_if_composite(pk)

        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)

        questions = []
        widgets = self._get_edit_widget(form=None)
        for question in item.questions:
            description = question.description_image_img()
            external_id = question.external_id
            current_question = {
                'error': False,
                'description': description,
                'external_id': external_id,
                'submit_text': None,
                'assignment_progress': None
            }
            # TODO: should be handled in Question class
            if question.type == QuestionType.one_of_six:
                current_question['cells'] = [
                    question.get_option_image(question.option1_image),
                    question.get_option_image(question.option2_image),
                    question.get_option_image(question.option3_image),
                    question.get_option_image(question.option4_image),
                    question.get_option_image(question.option5_image),
                    question.get_option_image(question.option6_image),
                ]
            elif question.type == QuestionType.two_of_five:
                current_question['cells'] = [
                    question.get_option_image(question.option1_image),
                    question.get_option_image(question.option2_image),
                    question.get_option_image(question.option3_image),
                    question.get_option_image(question.option4_image),
                    question.get_option_image(question.option5_image),
                ]
            elif question.type == QuestionType.three_to_three:
                current_question['cellsets'] = [
                    (
                        '1',
                        {'fields': ['checkbox1a', 'checkbox1b', 'checkbox1c']}
                    ),
                    (
                        '2',
                        {'fields': ['checkbox2a', 'checkbox2b', 'checkbox2c']}
                    ),
                ]

                current_question['cells'] = {
                    'checkbox1a': question.get_option_small_image(question.option1a_image),
                    'checkbox1b': question.get_option_small_image(question.option1b_image),
                    'checkbox1c': question.get_option_small_image(question.option1c_image),
                    'checkbox2a': question.get_option_small_image(question.option2a_image),
                    'checkbox2b': question.get_option_small_image(question.option2b_image),
                    'checkbox2c': question.get_option_small_image(question.option2c_image),
                }
            elif question.type == QuestionType.select_four:
                current_question['cellsets'] = [
                    (
                        'Antworten',
                        {'fields': ['selection1', 'selection2',
                                    'selection3', 'selection4']}
                    ),
                    (
                        'Optionen',
                        {'fields': ['option1', 'option2',
                                    'option3', 'option4',
                                    'option5', 'option6']}
                    ),
                ]

                current_question['cells'] = {
                    'option1': question.get_option_small_image(question.option1_image),
                    'option2': question.get_option_small_image(question.option2_image),
                    'option3': question.get_option_small_image(question.option3_image),
                    'option4': question.get_option_small_image(question.option4_image),
                    'option5': question.get_option_small_image(question.option5_image),
                    'option6': question.get_option_small_image(question.option6_image),
                    'selection1': question.get_option_small_image(question.selection1_image),
                    'selection2': question.get_option_small_image(question.selection2_image),
                    'selection3': question.get_option_small_image(question.selection3_image),
                    'selection4': question.get_option_small_image(question.selection4_image),
                }

            questions.append(current_question)

        self.extra_args = {'questions': questions}
        return self.render_template('edit_additional_multiple.html', widgets=widgets)


class QuestionModelIncorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['', FilterQuestionByAnsweredCorrectness, False]]
    title = 'Aufgaben (falsch beantwortet)'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic', 'category']
    formatters_columns = {'id': link_formatter_question, 'topic': link_formatter_topic_abbr}
    page_size = 100


class QuestionModelCorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['', FilterQuestionByAnsweredCorrectness, True]]
    title = 'Aufgaben (richtig beantwortet)'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich', 'category': 'Kategorie'}
    list_columns = ['id', 'topic', 'category']
    formatters_columns = {'id': link_formatter_question, 'topic': link_formatter_topic_abbr}
    page_size = 100


class TopicModelView(ModelView):
    datamodel = SQLAInterface(Topic)


class CategoryModelAdminView(ModelView):
    datamodel = SQLAInterface(Category)
