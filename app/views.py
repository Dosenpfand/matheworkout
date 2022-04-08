from random import randrange
from flask_appbuilder import ModelView, BaseView, SimpleFormView, MultipleView, IndexView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterInFunction, FilterEqual
from flask_appbuilder.widgets import RenderTemplateWidget
from flask_appbuilder.models.sqla.filters import BaseFilter, get_field_setup_query
from flask import render_template, flash, redirect, url_for, Markup, g, request, Markup
from . import appbuilder, db
from .forms import Question2of5Form, Question1of6Form, Question3to3Form, QuestionSelfAssessedForm, Question2DecimalsForm, Question1DecimalForm, QuestionSelect4Form
from .models import Topic, Question, QuestionType
from .sec_models import ExtendedUser, AssocUserQuestion
from sqlalchemy.sql.expression import func, select
from wtforms import HiddenField


def link_formatter(external_id):
    url = url_for(f'ExtIdToForm.ext_id_to_form', ext_id=external_id)
    return Markup(f'<a href="{url}">{external_id}</a>')


def get_question(type):
    request_id = request.args.get('ext_id')

    if request_id:
        result = db.session.query(Question).filter_by(
            external_id=request_id, type=type).first()
    else:
        active_topic_ids = get_active_topics()
        filter_arg = Question.topic_id.in_(active_topic_ids)
        result = db.session.query(Question).order_by(
            func.random()).filter(filter_arg).filter_by(type=type).first()

    return result


def get_question_count(type):
    active_topic_ids = get_active_topics()
    filter_arg = Question.topic_id.in_(active_topic_ids)
    count = db.session.query(Question).order_by(
        func.random()).filter(filter_arg).filter_by(type=type).count()
    return count


def get_active_topics():
    topic_ids = [topic.id for topic in g.user.active_topics]

    # If no topic IDs set for this user
    if topic_ids == []:
        # Set all topic IDs
        results = db.session.query(Topic).all()
        topic_ids = [result.id for result in results]

    return topic_ids


class QuestionRandom(BaseView):
    route_base = "/"

    @has_access
    @expose("questionrandom/", methods=['POST', 'GET'])
    def question_random(self):
        type_id_to_form = {
            0: QuestionType.two_of_five.value,
            1: QuestionType.one_of_six.value,
            2: QuestionType.three_to_three.value,
            3: QuestionType.two_decimals.value,
            4: QuestionType.one_decimal.value,
            5: QuestionType.self_assessed.value,
            6: QuestionType.select_four.value,
        }

        type_id_to_count = {}
        for id, class_name in type_id_to_form.items():
            type_id_to_count[id] = get_question_count(class_name)

        total_count = sum(type_id_to_count.values())

        if total_count == 0:
            rand_form = 'Question2of5FormView'
        else:
            rand_id = randrange(0, total_count)

            if rand_id < type_id_to_count[0]:
                rand_form = 'Question2of5FormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1]):
                rand_form = 'Question1of6FormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2]):
                rand_form = 'Question3to3FormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2] + type_id_to_count[3]):
                rand_form = 'Question2DecimalsFormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2] + type_id_to_count[3] + type_id_to_count[4]):
                rand_form = 'Question1DecimalFormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2] + type_id_to_count[3] + type_id_to_count[4] + type_id_to_count[5]):
                rand_form = 'QuestionSelfAssessedFormView'
            else:
                rand_form = 'QuestionSelect4FormView'

        return redirect(url_for(f'{rand_form}.this_form_get'))


class ExtIdToForm(BaseView):
    route_base = "/"

    @has_access
    @expose("extidtoform/<ext_id>", methods=['GET'])
    def ext_id_to_form(self, ext_id):
        question = db.session.query(Question).filter_by(
            external_id=ext_id).first()
        type = question.type.value

        type_to_form = {
            QuestionType.two_of_five.value: 'Question2of5FormView',
            QuestionType.one_of_six.value: 'Question1of6FormView',
            QuestionType.three_to_three: 'Question3to3FormView',
            QuestionType.two_decimals.value: 'Question2DecimalsFormView',
            QuestionType.one_decimal.value: 'Question1DecimalFormView',
            QuestionType.self_assessed.value: 'QuestionSelfAssessedFormView',
            QuestionType.select_four.value: 'QuestionSelect4FormView',
        }

        form = type_to_form[type]
        url = url_for(f'{form}.this_form_get')

        return redirect(f'{url}?ext_id={ext_id}')


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.two_of_five.value]]
    title = '2 aus 5'
    add_columns = Question.cols_two_of_five
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.two_of_five.value)}
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter}


class Question1of6ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.two_decimals.value]]
    title = '1 aus 6'
    add_columns = Question.cols_one_of_six
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.one_of_six.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter}


class Question3to3ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.three_to_three.value]]
    title = 'Lückentext'
    add_columns = Question.cols_three_to_three
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.three_to_three.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter}


class Question2DecimalsModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.two_decimals.value]]
    title = 'Werteingabe zwei Zahlen'
    add_columns = Question.cols_two_decimals
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.two_decimals.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter}


class Question1DecimalModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.one_decimal.value]]
    title = 'Werteingabe eine Zahl'
    add_columns = Question.cols_one_decimal
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.one_decimal.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter}


class QuestionSelfAssessedModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.self_assessed.value]]
    title = 'Selbstkontrolle'
    add_columns = Question.cols_self_assessed
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.self_assessed.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'external_id': link_formatter}


class QuestionSelect4ModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics], [
        'type', FilterEqual, QuestionType.self_assessed.value]]
    title = 'Zuordnung'
    add_columns = Question.cols_select_four
    add_form_extra_fields = {'type': HiddenField(
        default=QuestionType.select_four.value)}
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'external_id': link_formatter}

class FilterQuestionByAnsweredCorrectness(BaseFilter):
    name = "Filters for incorrectly answered questions"
    arg_name = None

    def apply(self, query, is_answer_correct):
        return query.filter(Question.answered_users.any(user_id=g.user.id, is_answer_correct=is_answer_correct))

class QuestionModelView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = 'Aufgaben'
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    formatters_columns = {'external_id': link_formatter}


class QuestionModelIncorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics],
                    ['', FilterQuestionByAnsweredCorrectness, False]]
    title = 'Aufgaben'
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    formatters_columns = {'external_id': link_formatter}

class QuestionModelCorrectAnsweredView(ModelView):
    datamodel = SQLAInterface(Question)
    base_filters = [['topic_id', FilterInFunction, get_active_topics],
                    ['', FilterQuestionByAnsweredCorrectness, True]]
    title = 'Aufgaben'
    label_columns = {'description_image': 'Beschreibung',
                     'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    formatters_columns = {'external_id': link_formatter}


class TopicModelView(ModelView):
    datamodel = SQLAInterface(Topic)


class ExtendedEditWidget(RenderTemplateWidget):
    template = 'extended_form.html'


class QuestionSelfAssessedFormView(SimpleFormView):
    form = QuestionSelfAssessedForm
    form_title = 'Selbstkontrolle'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(
            QuestionType.self_assessed.value)

        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id

        answer_value = request.args.get('answer')
        if answer_value:
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'tried_questions': ExtendedUser.tried_questions + 1})
            db.session.commit()
        if answer_value == 'CORRECT':
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()

        self.extra_args = {'question': {
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(id=id).first()

        random_url = url_for('QuestionRandom.question_random')
        solution_img = result.solution_image_img()
        correct_link = f'<a class="btn btn-primary" href="{random_url}?answer=CORRECT">Richtig</a>'
        incorrect_link = f'<a class="btn btn-primary" href="{random_url}?answer=INCORRECT">Falsch</a>'
        description = Markup(f'{solution_img}')
        after_description = Markup(f'{correct_link} {incorrect_link}')

        self.extra_args = {'question': {
            'description': description,
            'after_description': after_description,
            'external_id': result.external_id,
            'submit_text': None},
            'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2of5FormView(SimpleFormView):
    form = Question2of5Form
    form_title = '2 aus 5'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()

        question_result = get_question(QuestionType.two_of_five.value)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.checkbox1.label.text = question_result.get_option_image(
                question_result.option1_image)
            form.checkbox2.label.text = question_result.get_option_image(
                question_result.option2_image)
            form.checkbox3.label.text = question_result.get_option_image(
                question_result.option3_image)
            form.checkbox4.label.text = question_result.get_option_image(
                question_result.option4_image)
            form.checkbox5.label.text = question_result.get_option_image(
                question_result.option5_image)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.two_of_five.value).first()
        form.checkbox1.label.text = result.get_option_image(
            result.option1_image)
        form.checkbox2.label.text = result.get_option_image(
            result.option2_image)
        form.checkbox3.label.text = result.get_option_image(
            result.option3_image)
        form.checkbox4.label.text = result.get_option_image(
            result.option4_image)
        form.checkbox5.label.text = result.get_option_image(
            result.option5_image)

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = 'Richtig'
        else:
            form.checkbox1.description = 'Falsch'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'Richtig'
        else:
            form.checkbox2.description = 'Falsch'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'Richtig'
        else:
            form.checkbox3.description = 'Falsch'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'Richtig'
        else:
            form.checkbox4.description = 'Falsch'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'Richtig'
        else:
            form.checkbox5.description = 'Falsch'

        if (form.checkbox1.data == result.option1_is_correct) and \
            (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
            (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'FALSCH!'

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question1of6FormView(SimpleFormView):
    form = Question1of6Form
    form_title = '1 aus 6'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.one_of_six.value)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.checkbox1.label.text = question_result.get_option_image(
                question_result.option1_image)
            form.checkbox2.label.text = question_result.get_option_image(
                question_result.option2_image)
            form.checkbox3.label.text = question_result.get_option_image(
                question_result.option3_image)
            form.checkbox4.label.text = question_result.get_option_image(
                question_result.option4_image)
            form.checkbox5.label.text = question_result.get_option_image(
                question_result.option5_image)
            form.checkbox6.label.text = question_result.get_option_image(
                question_result.option6_image)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.one_of_six.value).first()
        form.checkbox1.label.text = result.get_option_image(
            result.option1_image)
        form.checkbox2.label.text = result.get_option_image(
            result.option2_image)
        form.checkbox3.label.text = result.get_option_image(
            result.option3_image)
        form.checkbox4.label.text = result.get_option_image(
            result.option4_image)
        form.checkbox5.label.text = result.get_option_image(
            result.option5_image)
        form.checkbox6.label.text = result.get_option_image(
            result.option6_image)

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = 'Richtig'
        else:
            form.checkbox1.description = 'Falsch'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'Richtig'
        else:
            form.checkbox2.description = 'Falsch'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'Richtig'
        else:
            form.checkbox3.description = 'Falsch'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'Richtig'
        else:
            form.checkbox4.description = 'Falsch'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'Richtig'
        else:
            form.checkbox5.description = 'Falsch'
        if form.checkbox6.data == result.option6_is_correct:
            form.checkbox6.description = 'Richtig'
        else:
            form.checkbox6.description = 'Falsch'

        if (form.checkbox1.data == result.option1_is_correct) and \
            (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
            (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct) and \
                (form.checkbox6.data == result.option6_is_correct):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'FALSCH!'

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                           'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question3to3FormView(SimpleFormView):
    form = Question3to3Form
    form_title = 'Lückentext'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    form_fieldsets = [
        (
            '1',
            {'fields': ['checkbox1a', 'checkbox1b', 'checkbox1c']}
        ),
        (
            '2',
            {'fields': ['checkbox2a', 'checkbox2b', 'checkbox2c']}
        ),
    ]

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(
            QuestionType.three_to_three.value)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.checkbox1a.label.text = question_result.get_option_image(
                question_result.option1a_image)
            form.checkbox1b.label.text = question_result.get_option_image(
                question_result.option1b_image)
            form.checkbox1c.label.text = question_result.get_option_image(
                question_result.option1c_image)
            form.checkbox2a.label.text = question_result.get_option_image(
                question_result.option2a_image)
            form.checkbox2b.label.text = question_result.get_option_image(
                question_result.option2b_image)
            form.checkbox2c.label.text = question_result.get_option_image(
                question_result.option2c_image)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.three_to_three.value).first()
        form.checkbox1a.label.text = result.get_option_image(
            result.option1a_image)
        form.checkbox1b.label.text = result.get_option_image(
            result.option1b_image)
        form.checkbox1c.label.text = result.get_option_image(
            result.option1c_image)
        form.checkbox2a.label.text = result.get_option_image(
            result.option2a_image)
        form.checkbox2b.label.text = result.get_option_image(
            result.option2b_image)
        form.checkbox2c.label.text = result.get_option_image(
            result.option2c_image)

        if form.checkbox1a.data == result.option1a_is_correct:
            form.checkbox1a.description = 'Richtig'
        else:
            form.checkbox1a.description = 'Falsch'
        if form.checkbox1b.data == result.option1b_is_correct:
            form.checkbox1b.description = 'Richtig'
        else:
            form.checkbox1b.description = 'Falsch'
        if form.checkbox1c.data == result.option1c_is_correct:
            form.checkbox1c.description = 'Richtig'
        else:
            form.checkbox1c.description = 'Falsch'
        if form.checkbox2a.data == result.option2a_is_correct:
            form.checkbox2a.description = 'Richtig'
        else:
            form.checkbox2a.description = 'Falsch'
        if form.checkbox2b.data == result.option2b_is_correct:
            form.checkbox2b.description = 'Richtig'
        else:
            form.checkbox2b.description = 'Falsch'
        if form.checkbox2c.data == result.option2c_is_correct:
            form.checkbox2c.description = 'Richtig'
        else:
            form.checkbox2c.description = 'Falsch'

        if (form.checkbox1a.data == result.option1a_is_correct) and \
            (form.checkbox1b.data == result.option1b_is_correct) and \
                (form.checkbox1c.data == result.option1c_is_correct) and \
            (form.checkbox2a.data == result.option2a_is_correct) and \
                (form.checkbox2b.data == result.option2b_is_correct) and \
                (form.checkbox2c.data == result.option2c_is_correct):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'FALSCH!'

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2DecimalsFormView(SimpleFormView):
    form = Question2DecimalsForm
    form_title = 'Werteingabe zwei Zahlen'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.two_decimals.value)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.value1.label.text = 'Ergebnis 1'
            form.value2.label.text = 'Ergebnis 2'

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.two_decimals.value).first()
        form.value1.label.text = 'Ergebnis 1'
        form.value2.label.text = 'Ergebnis 2'
        value1_correct = False
        value2_correct = False

        if (form.value1.data <= result.value1_upper_limit) and (form.value1.data >= result.value1_lower_limit):
            form.value1.description = 'Richtig'
            value1_correct = True
        else:
            form.value1.description = 'Falsch'

        if (form.value2.data <= result.value2_upper_limit) and (form.value2.data >= result.value2_lower_limit):
            form.value2.description = 'Richtig'
            value2_correct = True
        else:
            form.value2.description = 'Falsch'

        if value1_correct and value2_correct:
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = f'FALSCH! Richtig gewesen wäre: {result.value1_lower_limit} <= Ergebnis 1 <= {result.value1_upper_limit}, {result.value2_lower_limit} <= Ergebnis 2 <= {result.value2_upper_limit}'

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

class Question1DecimalFormView(SimpleFormView):
    form = Question1DecimalForm
    form_title = 'Werteingabe eine Zahl'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.one_decimal.value)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False
            form.value.label.text = 'Ergebnis 1'

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.one_decimal.value).first()
        form.value.label.text = 'Ergebnis'
        message = 'FALSCH!'

        if (form.value.data <= result.value1_upper_limit) and (form.value.data >= result.value1_lower_limit):
            form.value.description = 'Richtig'
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
            is_answer_correct = True
        else:
            message = f'FALSCH! Richtig gewesen wäre: {result.value1_lower_limit} <= Ergebnis <= {result.value1_upper_limit}'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        # TODO: for all question types
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)

        # TODO: for all commits
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error(c.LOGMSG_ERR_SEC_UPD_USER.format(str(e)))

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class QuestionSelect4FormView(SimpleFormView):
    form = QuestionSelect4Form
    form_title = 'Zuordnung'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    form_fieldsets = [
        (
            'Antworten',
            {'fields': ['selection1', 'selection2',
                        'selection3', 'selection4']}
        ),
    ]

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.select_four)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            options = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            options = {'A': question_result.get_option_image(question_result.option1_image),
                       'B': question_result.get_option_image(question_result.option2_image),
                       'C': question_result.get_option_image(question_result.option3_image),
                       'D': question_result.get_option_image(question_result.option4_image),
                       'E': question_result.get_option_image(question_result.option5_image),
                       'F': question_result.get_option_image(question_result.option6_image)}
            error = False

            form.selection1.label.text = question_result.get_selection_image(
                question_result.selection1_image)
            form.selection2.label.text = question_result.get_selection_image(
                question_result.selection2_image)
            form.selection3.label.text = question_result.get_selection_image(
                question_result.selection3_image)
            form.selection4.label.text = question_result.get_selection_image(
                question_result.selection4_image)

        self.extra_args = \
            {'question': {'error': error,
                          'description': description,
                          'options': options,
                          'external_id': external_id,
                          'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.select_four.value).first()
        form.selection1.label.text = result.get_selection_image(
            result.selection1_image)
        form.selection2.label.text = result.get_selection_image(
            result.selection2_image)
        form.selection3.label.text = result.get_selection_image(
            result.selection3_image)
        form.selection4.label.text = result.get_selection_image(
            result.selection4_image)

        if form.selection1.data == result.selection1_solution.value:
            form.selection1.description = 'Richtig'
        else:
            form.selection1.description = 'Falsch'
        if form.selection2.data == result.selection2_solution.value:
            form.selection2.description = 'Richtig'
        else:
            form.selection2.description = 'Falsch'
        if form.selection3.data == result.selection3_solution.value:
            form.selection3.description = 'Richtig'
        else:
            form.selection3.description = 'Falsch'
        if form.selection4.data == result.selection4_solution.value:
            form.selection4.description = 'Richtig'
        else:
            form.selection4.description = 'Falsch'

        if (form.selection1.data == result.selection1_solution.value) and \
            (form.selection2.data == result.selection2_solution.value) and \
            (form.selection3.data == result.selection3_solution.value) and \
                (form.selection4.data == result.selection4_solution.value):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'FALSCH!'

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )

class AssocUserQuestionModelView(ModelView):
    datamodel = SQLAInterface(AssocUserQuestion)
    list_columns = ['user', 'question', 'created_on', 'is_answer_correct']

appbuilder.add_view(
    AssocUserQuestionModelView,
    "Beantwortete Fragen",
    icon="fa-question",
    category="Security",
    category_icon="fa-question")


db.create_all()
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
appbuilder.add_view(
    TopicModelView,
    "Grundkompetenzbereiche",
    icon="fa-align-justify",
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
appbuilder.add_view(
    QuestionModelIncorrectAnsweredView,
    "Falsch beantwortete Aufgaben",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
appbuilder.add_view(
    QuestionModelCorrectAnsweredView,
    "Richtig beantwortete Aufgaben",
    icon="fa-align-justify",
    category="Aufgabenlisten",
    category_icon="fa-align-justify",
)
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

appbuilder.add_view_no_menu(QuestionRandom())
appbuilder.add_link(
    "Zufall", href="/questionrandom/", icon="fa-question", category="Zufallsaufgaben", category_icon="fa-question"
)
appbuilder.add_view_no_menu(ExtIdToForm())

# TODO: activate?
# appbuilder.security_cleanup()
