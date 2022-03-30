from random import randrange
from flask_appbuilder import ModelView, BaseView, SimpleFormView, MultipleView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from flask import render_template, flash, redirect, url_for, Markup, g, request, Markup
from . import appbuilder, db
from .forms import Question2of5Form, Question1of6Form, Question3to3Form, TopicForm, QuestionSelfAssessedForm, Question2DecimalsForm, Question1DecimalForm, QuestionSelect4Form
from .models import Question2of5, Question1of6, Question3to3, Topic, QuestionSelfAssessed, Question2Decimals, Question1Decimal, QuestionSelect4
from .sec_models import ExtendedUser
from flask_appbuilder.security.views import UserDBModelView
from flask_babel import lazy_gettext
from sqlalchemy.sql.expression import func, select

def get_user():
    return g.user

def link_formatter_2_of_5(value):
    return Markup('<a href="' + url_for('Question2of5FormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question2of5)

    label_columns = {'description_image': 'Description Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter_2_of_5}

def link_formatter_1_of_6(value):
    return Markup('<a href="' + url_for('Question1of6FormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class Question1of6ModelView(ModelView):
    datamodel = SQLAInterface(Question1of6)

    label_columns = {'description_image': 'Description Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter_1_of_6 }

def link_formatter_3_to_3(value):
    return Markup('<a href="' + url_for('Question3to3FormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class Question3to3ModelView(ModelView):
    datamodel = SQLAInterface(Question3to3)

    label_columns = {'description_image': 'Description Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter_3_to_3 }

def link_formatter_2_decimals(value):
    return Markup('<a href="' + url_for('Question2DecimalsFormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class Question2DecimalsModelView(ModelView):
    datamodel = SQLAInterface(Question2Decimals)

    label_columns = {'description_image': 'Description Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter_2_decimals }

def link_formatter_1_decimal(value):
    return Markup('<a href="' + url_for('Question1DecimalFormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class Question1DecimalModelView(ModelView):
    datamodel = SQLAInterface(Question1Decimal)

    label_columns = {'description_image': 'Description Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'title']
    formatters_columns = {'external_id': link_formatter_1_decimal }

def link_formatter_self_assessed(value):
    return Markup('<a href="' + url_for('QuestionSelfAssessedFormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class QuestionSelfAssessedModelView(ModelView):
    datamodel = SQLAInterface(QuestionSelfAssessed)

    label_columns = {'description_image': 'Description Image',
                     'solution_image': 'Solution Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'external_id': link_formatter_self_assessed }

def link_formatter_select_4(value):
    return Markup('<a href="' + url_for('QuestionSelect4FormView.this_form_get') + '?ext_id=' + str(value) + '">' + str(value) + '</a>')

class QuestionSelect4ModelView(ModelView):
    datamodel = SQLAInterface(QuestionSelect4)

    label_columns = {'description_image': 'Description Image',
                     'solution_image': 'Solution Image'}
    list_columns = ['external_id', 'topic']
    show_columns = ['description_image_img', 'solution_image_img']
    formatters_columns = {'external_id': link_formatter_select_4 }

class QuestionMultipleView(MultipleView):
    views = [Question2of5ModelView, Question1of6ModelView, Question3to3ModelView, Question2DecimalsModelView, Question1DecimalModelView, QuestionSelfAssessed]


class TopicModelView(ModelView):
    datamodel = SQLAInterface(Topic)


class TopicFormView(SimpleFormView):
    form = TopicForm

    def form_get(self, form):
        self.update_redirect()
        result = db.session.query(Topic)
        choices = []
        for element in result:
            choices += [(element.id, element.name)]
        form.topic.choices = choices

    def form_post(self, form):
        self.update_redirect()
        result = db.session.query(Topic)
        choices = []
        for element in result:
            choices += [(element.id, element.name)]
        form.topic.choices = choices
        flash('test', 'info')

        # form.topic.label = str(form.topic.data)


class QuestionSelfAssessedFormView(SimpleFormView):
    form = QuestionSelfAssessedForm
    form_title = 'Self Assessed Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(QuestionSelfAssessed).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(QuestionSelfAssessed).order_by(func.random()).first()

        form.id.data = result.id

        answer_value = request.args.get('answer')
        if answer_value:
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
            db.session.commit()
        if answer_value == 'CORRECT':
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()

        self.extra_args = {'question': {
            'description': result.description_image_img(),
            'external_id': result.external_id}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(
            QuestionSelfAssessed).filter_by(id=id).first()

        self.extra_args = {'question': {'description': result.solution_image_img(
        ) + Markup('<a href="' + url_for('QuestionSelfAssessedFormView.this_form_get') + '?answer=CORRECT">CORRECT</a> <a href="' + url_for('QuestionSelfAssessedFormView.this_form_get') + '?answer=INCORRECT">INCORRECT</a>'),
            'external_id': result.external_id}}

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
    form_title = '2 of 5 Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()

        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(Question2of5).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(Question2of5).order_by(func.random()).first()

        form.id.data = result.id

        form.id.data = result.id
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

        self.extra_args = {'question': {
            'description': result.description_image_img(),
            'external_id': result.external_id}}

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
            form.checkbox1.description = 'correct'
        else:
            form.checkbox1.description = 'incorrect'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'correct'
        else:
            form.checkbox2.description = 'incorrect'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'correct'
        else:
            form.checkbox3.description = 'incorrect'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'correct'
        else:
            form.checkbox4.description = 'incorrect'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'correct'
        else:
            form.checkbox5.description = 'incorrect'

        if (form.checkbox1.data == result.option1_is_correct) and \
            (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
            (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct):
            message = 'CORRECT!'
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'INCORRECT!'

        user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST',
            'external_id': result.external_id}}

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
    form_title = '1 of 6 Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(Question1of6).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(Question1of6).order_by(func.random()).first()

        form.id.data = result.id

        form.id.data = result.id
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

        self.extra_args = {'question': {
            'description': result.description_image_img(),
            'external_id': result.external_id}}

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
            form.checkbox1.description = 'correct'
        else:
            form.checkbox1.description = 'incorrect'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'correct'
        else:
            form.checkbox2.description = 'incorrect'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'correct'
        else:
            form.checkbox3.description = 'incorrect'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'correct'
        else:
            form.checkbox4.description = 'incorrect'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'correct'
        else:
            form.checkbox5.description = 'incorrect'
        if form.checkbox6.data == result.option6_is_correct:
            form.checkbox6.description = 'correct'
        else:
            form.checkbox6.description = 'incorrect'

        if (form.checkbox1.data == result.option1_is_correct) and \
            (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
            (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct) and \
                (form.checkbox6.data == result.option6_is_correct):
            message = 'CORRECT!'
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'INCORRECT!'

        user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST'},
            'external_id': result.external_id}

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
    form_title = '3 to 3 Test'
    form_template = 'edit_additional.html'

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
        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(Question3to3).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(Question3to3).order_by(func.random()).first()
        form.id.data = result.id

        form.id.data = result.id
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
        self.extra_args = {'question': {
            'description': result.description_image_img(),
            'external_id': result.external_id}}

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
            form.checkbox1a.description = 'correct'
        else:
            form.checkbox1a.description = 'incorrect'
        if form.checkbox1b.data == result.option1b_is_correct:
            form.checkbox1b.description = 'correct'
        else:
            form.checkbox1b.description = 'incorrect'
        if form.checkbox1c.data == result.option1c_is_correct:
            form.checkbox1c.description = 'correct'
        else:
            form.checkbox1c.description = 'incorrect'
        if form.checkbox2a.data == result.option2a_is_correct:
            form.checkbox2a.description = 'correct'
        else:
            form.checkbox2a.description = 'incorrect'
        if form.checkbox2b.data == result.option2b_is_correct:
            form.checkbox2b.description = 'correct'
        else:
            form.checkbox2b.description = 'incorrect'
        if form.checkbox2c.data == result.option2c_is_correct:
            form.checkbox2c.description = 'correct'
        else:
            form.checkbox2c.description = 'incorrect'

        if (form.checkbox1a.data == result.option1a_is_correct) and \
            (form.checkbox1b.data == result.option1b_is_correct) and \
                (form.checkbox1c.data == result.option1c_is_correct) and \
            (form.checkbox2a.data == result.option2a_is_correct) and \
                (form.checkbox2b.data == result.option2b_is_correct) and \
                (form.checkbox2c.data == result.option2c_is_correct):
            message = 'CORRECT!'
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'INCORRECT!'

        user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST',
            'external_id': result.external_id}}

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
    form_title = '2 Decimals Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(Question2Decimals).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(Question2Decimals).order_by(func.random()).first()

        form.id.data = result.id

        form.id.data = result.id
        form.value1.label.text = 'Ergebnis 1'
        form.value2.label.text = 'Ergebnis 2'

        self.extra_args = {'question': {
            'description': result.description_image_img(),
            'external_id': result.external_id}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question2Decimals).filter_by(id=id).first()
        form.value1.label.text = 'Ergebnis 1'
        form.value2.label.text = 'Ergebnis 2'
        value1_correct = False
        value2_correct = False

        if (form.value1.data <= result.value1_upper_limit) and (form.value1.data >= result.value1_lower_limit):
            form.value1.description = 'correct'
            value1_correct = True
        else:
            form.value1.description = 'incorrect'

        if (form.value2.data <= result.value2_upper_limit) and (form.value2.data >= result.value2_lower_limit):
            form.value2.description = 'correct'
            value2_correct = True
        else:
            form.value2.description = 'incorrect'

        if value1_correct and value2_correct:
            message = 'CORRECT!'
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'INCORRECT!'

        user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST',
            'external_id': result.external_id}}

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
    form_title = '1 Decimal Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(Question1Decimal).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(Question1Decimal).order_by(func.random()).first()

        form.id.data = result.id

        form.id.data = result.id
        form.value.label.text = 'Ergebnis 1'

        self.extra_args = {'question': {
            'description': result.description_image_img(),
            'external_id': result.external_id}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question1Decimal).filter_by(id=id).first()
        form.value.label.text = 'Ergebnis 1'
        message = 'INCORRECT!'

        if (form.value.data <= result.value_upper_limit) and (form.value.data >= result.value_lower_limit):
            form.value.description = 'correct'
            message = 'CORRECT!'
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'INCORRECT!'

        user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST',
            'external_id': result.external_id}}

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
    form_title = 'Select 4 Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        request_id = request.args.get('ext_id')
        if request_id:
            result = db.session.query(QuestionSelect4).filter_by(external_id=request_id).first()
        else:
            result = db.session.query(QuestionSelect4).order_by(func.random()).first()
        form.id.data = result.id

        form.id.data = result.id
        form.selection1.label.text = result.get_selection_image(
            result.selection1_image)
        form.selection2.label.text = result.get_selection_image(
            result.selection2_image)
        form.selection3.label.text = result.get_selection_image(
            result.selection3_image)
        form.selection4.label.text = result.get_selection_image(
            result.selection4_image)

        self.extra_args = \
        {'question': {'description': result.description_image_img(),
                      'options': {'A': result.get_option_image(result.option1_image),
                                  'B': result.get_option_image(result.option2_image),
                                  'C': result.get_option_image(result.option3_image),
                                  'D': result.get_option_image(result.option4_image),
                                  'E': result.get_option_image(result.option5_image),
                                  'F': result.get_option_image(result.option6_image)},
                                  'external_id': result.external_id}}

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
            form.selection1.description = 'correct'
        else:
            form.selection1.description = 'incorrect'
        if form.selection2.data == result.selection2_solution.value:
            form.selection2.description = 'correct'
        else:
            form.selection2.description = 'incorrect'
        if form.selection3.data == result.selection3_solution.value:
            form.selection3.description = 'correct'
        else:
            form.selection3.description = 'incorrect'
        if form.selection4.data == result.selection4_solution.value:
            form.selection4.description = 'correct'
        else:
            form.selection4.description = 'incorrect'

        if (form.selection1.data == result.selection1_solution.value) and \
            (form.selection2.data == result.selection2_solution.value) and \
            (form.selection3.data == result.selection3_solution.value) and \
                (form.selection4.data == result.selection4_solution.value):
            message = 'CORRECT!'
            user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
        else:
            message = 'INCORRECT!'

        user_result = db.session.query(ExtendedUser).filter_by(id=get_user().id).update({'tried_questions': ExtendedUser.tried_questions + 1})
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST',
            'external_id': result.external_id}}

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
    "List 2 out of 5 questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    Question1of6ModelView,
    "List 1 out of 6 questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    Question3to3ModelView,
    "List 3 to 3 questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    Question2DecimalsModelView,
    "List 2 decimals questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    Question1DecimalModelView,
    "List 1 decimal questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    QuestionSelfAssessedModelView,
    "List self assessed questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    QuestionSelect4ModelView,
    "List select 4 questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    TopicModelView,
    "List Topics",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    QuestionMultipleView,
    "List all questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    TopicFormView,
    "Choose Topic",
    icon="fa-group",
    label=_("Choose Topic"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    Question2of5FormView,
    "2 of 5 Test",
    icon="fa-group",
    label=_("2 of 5 Test"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    Question1of6FormView(),
    "1 of 6 Test",
    icon="fa-group",
    label=_("1 of 6 Test"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    Question3to3FormView(),
    "3 to 3 Test",
    icon="fa-group",
    label=_("3 to 3 Test"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    Question2DecimalsFormView(),
    "2 Decimals Test",
    icon="fa-group",
    label=_("2 Decimals Test"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    Question1DecimalFormView(),
    "1 Decimal Test",
    icon="fa-group",
    label=_("1 Decimal Test"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    QuestionSelfAssessedFormView,
    "Self Assessed Test",
    icon="fa-group",
    label=_("Self Assessed Test"),
    category="Tests",
    category_icon="fa-cogs")
appbuilder.add_view(
    QuestionSelect4FormView,
    "Select 4 Test",
    icon="fa-group",
    label=_("Select 4 Test"),
    category="Tests",
    category_icon="fa-cogs")
