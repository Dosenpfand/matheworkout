from random import randrange
from flask_appbuilder import ModelView, BaseView, SimpleFormView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from flask import render_template, flash, redirect, url_for, Markup
from . import appbuilder, db
from .forms import Question2of5Form, Question1of6Form, TopicForm, QuestionSelfAssessedForm
from .models import Question2of5, Question1of6, Topic, QuestionSelfAssessed
from flask_appbuilder.security.views import UserDBModelView
from flask_babel import lazy_gettext

class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question2of5)

    label_columns = {'description_image':'Description Image'}
    # list_columns = ['photo_img_thumbnail', 'name']
    show_columns = ['description_image_img','title']

class Question1of6ModelView(ModelView):
    datamodel = SQLAInterface(Question1of6)

    label_columns = {'description_image':'Description Image'}
    # list_columns = ['photo_img_thumbnail', 'name']
    show_columns = ['description_image_img','title']

class QuestionSelfAssessedModelView(ModelView):
    datamodel = SQLAInterface(QuestionSelfAssessed)

    label_columns = {'description_image':'Description Image', 'solution_image':'Solution Image'}
    # list_columns = ['photo_img_thumbnail', 'name']
    show_columns = ['description_image_img','solution_image_img']

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
        # Get random question
        # TODO: no gaps in ID allowed!
        count = db.session.query(QuestionSelfAssessed).count()
        id = randrange(1, count + 1)
        result = db.session.query(QuestionSelfAssessed).filter_by(id=id).first()

        form.id.data = id

        self.extra_args = {'question': {'description': result.description_image_img()}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(QuestionSelfAssessed).filter_by(id=id).first()

        self.extra_args = {'question': {'description': result.solution_image_img() + Markup('<a href="/correct">CORRECT</a> <a href="/correct">INCORRECT</a>')}}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
                    self.form_template,
                    title=self.form_title,
                    widgets=widgets,
                    appbuilder=self.appbuilder,
                )
        # return redirect(url_for('Question2of5EvaluateView.evaluate'))  # , id=DBTable.id))


class Question2of5FormView(SimpleFormView):
    form = Question2of5Form
    form_title = '2 of 5 Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        # Get random question
        # TODO: no gaps in ID allowed!
        count = db.session.query(Question2of5).count()
        id = randrange(1, count + 1)
        result = db.session.query(Question2of5).filter_by(id=id).first()

        form.id.data = id
        form.checkbox1.label.text = result.get_option_image(result.option1_image)
        form.checkbox2.label.text = result.get_option_image(result.option2_image)
        form.checkbox3.label.text = result.get_option_image(result.option3_image)
        form.checkbox4.label.text = result.get_option_image(result.option4_image)
        form.checkbox5.label.text = result.get_option_image(result.option5_image)

        self.extra_args = {'question': {'description': result.description_image_img()}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question2of5).filter_by(id=id).first()
        form.checkbox1.label.text = result.get_option_image(result.option1_image)
        form.checkbox2.label.text = result.get_option_image(result.option2_image)
        form.checkbox3.label.text = result.get_option_image(result.option3_image)
        form.checkbox4.label.text = result.get_option_image(result.option4_image)
        form.checkbox5.label.text = result.get_option_image(result.option5_image)


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
        else:
            message = 'INCORRECT!'
        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST'}}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
                    self.form_template,
                    title=self.form_title,
                    widgets=widgets,
                    appbuilder=self.appbuilder,
                )
        # return redirect(url_for('Question2of5EvaluateView.evaluate'))  # , id=DBTable.id))

class Question1of6FormView(SimpleFormView):
    form = Question1of6Form
    form_title = '1 of 6 Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        # Get random question
        # TODO: no gaps in ID allowed!
        count = db.session.query(Question1of6).count()
        id = randrange(1, count + 1)
        result = db.session.query(Question1of6).filter_by(id=id).first()

        form.id.data = id
        form.checkbox1.label.text = result.get_option_image(result.option1_image)
        form.checkbox2.label.text = result.get_option_image(result.option2_image)
        form.checkbox3.label.text = result.get_option_image(result.option3_image)
        form.checkbox4.label.text = result.get_option_image(result.option4_image)
        form.checkbox5.label.text = result.get_option_image(result.option5_image)
        form.checkbox6.label.text = result.get_option_image(result.option6_image)

        self.extra_args = {'question': {'description': result.description_image_img()}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question1of6).filter_by(id=id).first()
        form.checkbox1.label.text = result.get_option_image(result.option1_image)
        form.checkbox2.label.text = result.get_option_image(result.option2_image)
        form.checkbox3.label.text = result.get_option_image(result.option3_image)
        form.checkbox4.label.text = result.get_option_image(result.option4_image)
        form.checkbox5.label.text = result.get_option_image(result.option5_image)
        form.checkbox6.label.text = result.get_option_image(result.option6_image)


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
        else:
            message = 'INCORRECT!'
        flash(message, 'info')

        self.extra_args = {'question': {'description': 'TEST'}}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
                    self.form_template,
                    title=self.form_title,
                    widgets=widgets,
                    appbuilder=self.appbuilder,
                )
        # return redirect(url_for('Question2of5EvaluateView.evaluate'))  # , id=DBTable.id))

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
    QuestionSelfAssessedModelView,
    "List self assessed questions",
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
    QuestionSelfAssessedFormView,
    "Self Assessed Test",
    icon="fa-group",
    label=_("Self Assessed Test"),
    category="Tests",
    category_icon="fa-cogs")
