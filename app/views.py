from random import randrange
from flask_appbuilder import ModelView, BaseView, SimpleFormView, MultipleView, IndexView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterInFunction
from flask_appbuilder.widgets import RenderTemplateWidget
from flask_babel import lazy_gettext as _
from flask import render_template, flash, redirect, url_for, Markup, g, request, Markup
from . import appbuilder, db
from .forms import Question2of5Form, Question1of6Form, Question3to3Form, QuestionSelfAssessedForm, Question2DecimalsForm, Question1DecimalForm, QuestionSelect4Form
from .models import Question2of5, Question1of6, Question3to3, Topic, QuestionSelfAssessed, Question2Decimals, Question1Decimal, QuestionSelect4
from .sec_models import ExtendedUser
from flask_appbuilder.security.views import UserDBModelView
from flask_babel import lazy_gettext
from sqlalchemy.sql.expression import func, select
import logging


def link_formatter(form_view_name, external_id):
    form_url = url_for(f'{form_view_name}.this_form_get')
    return Markup(f'<a href="{form_url}?ext_id={external_id}">{external_id}</a>')


def get_question(question_model):
    request_id = request.args.get('ext_id')

    if request_id:
        result = db.session.query(question_model).filter_by(
            external_id=request_id).first()
    else:
        active_topic_ids = get_active_topics()
        filter_arg = question_model.topic_id.in_(active_topic_ids)
        result = db.session.query(question_model).order_by(
            func.random()).filter(filter_arg).first()

    return result

def get_question_count(question_model):
    active_topic_ids = get_active_topics()
    filter_arg = question_model.topic_id.in_(active_topic_ids)
    count = db.session.query(question_model).order_by(
        func.random()).filter(filter_arg).count()
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
            0: Question2of5,
            1: Question1of6,
            2: Question3to3,
            3: Question2Decimals,
            4: Question1Decimal,
            5: QuestionSelfAssessed,
            6: QuestionSelect4,
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


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question2of5)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = '2 aus 5'
    list_title = title
    show_title = title
    add_title = title
    edit_title = title
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'Question2of5FormView', value)}


class Question1of6ModelView(ModelView):
    datamodel = SQLAInterface(Question1of6)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = '1 aus 6'
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'Question1of6FormView', value)}


class Question3to3ModelView(ModelView):
    datamodel = SQLAInterface(Question3to3)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = 'Lückentext'
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'Question3to3FormView', value)}


class Question2DecimalsModelView(ModelView):
    datamodel = SQLAInterface(Question2Decimals)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = 'Werteingabe zwei Zahlen'
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'Question2DecimalsFormView', value)}


class Question1DecimalModelView(ModelView):
    datamodel = SQLAInterface(Question1Decimal)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = 'Werteingabe eine Zahl'
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'Question1DecimalFormView', value)}


class QuestionSelfAssessedModelView(ModelView):
    datamodel = SQLAInterface(QuestionSelfAssessed)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = 'Selbstkontrolle'
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'QuestionSelfAssessedFormView', value)}


class QuestionSelect4ModelView(ModelView):
    datamodel = SQLAInterface(QuestionSelect4)

    base_filters = [['topic_id', FilterInFunction, get_active_topics]]
    title = 'Zuordnung'
    label_columns = {'description_image': 'Beschreibung', 'external_id': 'Frage Nr.', 'topic': 'Grundkompetenzbereich'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'external_id': lambda value: link_formatter(
        'QuestionSelect4FormView', value)}


class QuestionMultipleView(MultipleView):
    views = [Question2of5ModelView, Question1of6ModelView, Question3to3ModelView,
             Question2DecimalsModelView, Question1DecimalModelView, QuestionSelfAssessedModelView,
             QuestionSelect4ModelView]


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
        question_result = get_question(QuestionSelfAssessed)

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
        result = db.session.query(
            QuestionSelfAssessed).filter_by(id=id).first()

        random_url = url_for(f'QuestionRandom.question_random')
        solution_img = result.solution_image_img()
        correct_link = f'<a href="{random_url}?answer=CORRECT">RICHTIG</a>'
        incorrect_link = f'<a href="{random_url}?answer=INCORRECT">FALSCH</a>'
        description = Markup(f'{solution_img} {correct_link} {incorrect_link}')

        self.extra_args = {'question': {
            'description': description, 'external_id': result.external_id,
            'submit_text': None},
            'form_action': url_for(f'QuestionRandom.question_random')}

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

        question_result = get_question(Question2of5)
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
        result = db.session.query(Question2of5).filter_by(id=id).first()
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
                           'form_action': url_for(f'QuestionRandom.question_random')}

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
        question_result = get_question(Question1of6)
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
        result = db.session.query(Question1of6).filter_by(id=id).first()
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
                           'form_action': url_for(f'QuestionRandom.question_random')}

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
        question_result = get_question(Question3to3)
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
        result = db.session.query(Question3to3).filter_by(id=id).first()
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
                           'form_action': url_for(f'QuestionRandom.question_random')}

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
        question_result = get_question(Question2Decimals)
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
        result = db.session.query(Question2Decimals).filter_by(id=id).first()
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
                           'form_action': url_for(f'QuestionRandom.question_random')}

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
        question_result = get_question(Question1Decimal)
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
        result = db.session.query(Question1Decimal).filter_by(id=id).first()
        form.value.label.text = 'Ergebnis'
        message = 'FALSCH!'

        if (form.value.data <= result.value_upper_limit) and (form.value.data >= result.value_lower_limit):
            form.value.description = 'Richtig'
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = f'FALSCH! Richtig gewesen wäre: {result.value_lower_limit} <= Ergebnis <= {result.value_upper_limit}'

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for(f'QuestionRandom.question_random')}

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
            {'fields': ['selection1', 'selection2', 'selection3', 'selection4']}
        ),
    ]

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionSelect4)
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
        result = db.session.query(QuestionSelect4).filter_by(id=id).first()
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
                           'form_action': url_for(f'QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


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
    QuestionMultipleView,
    "Alle Aufgaben",
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

appbuilder.security_cleanup()
